"""Lazy replacement of registered battle BG planes at original scrolling UVs.

The game keeps ownership of sprites, effects and HUD pixels. Identification
uses the original layer's RGB555 palette and its live hardware scroll offsets.
"""
import argparse,json,time,zlib
from pathlib import Path
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image,ImageFilter

ROOT=Path(__file__).resolve().parent.parent
FOLDER=ROOT/'graphics/battle_backgrounds'

def rgb555(a):
    r=a[:,:,0].astype('uint16')>>3;g=a[:,:,1].astype('uint16')>>3;b=a[:,:,2].astype('uint16')>>3
    return r|(g<<5)|(b<<10)

def compile_native_index():
    """Asset-time preparation; never decode all reference PNGs during play."""
    catalog=json.loads((FOLDER/'catalog.json').read_text(encoding='utf-8'));rows=catalog['resources'];out=FOLDER/'runtime_index';out.mkdir(exist_ok=True)
    references=np.zeros((len(rows),256,256),dtype='uint16');names=[];sizes=[];layers=[]
    for i,row in enumerate(rows):
        a=np.asarray(Image.open(ROOT/'graphics'/row['native']).convert('RGBA'));h,w=a.shape[:2]
        assert w<=256 and h<=256,(row['name'],w,h)
        q=rgb555(a)|((a[:,:,3]>0).astype('uint16')<<15);references[i,:h,:w]=q;names.append(row['name']);sizes.append([w,h]);layers.append(sorted(set(u['layer'] for u in row['uses'])))
    temporary=out/'references.tmp.npy';np.save(temporary,references);temporary.replace(out/'references.npy')
    meta=dict(version=1,names=names,sizes=sizes,layers=layers);temporary=out/'index.tmp.json';temporary.write_text(json.dumps(meta,indent=2));temporary.replace(out/'index.json');print('Prepared',len(rows),'battle BG references')

def prepare_texture(item,owner,size,hardware):
    """Read only the winning art, then prepare its current display dimensions."""
    with Image.open(ROOT/'graphics'/item['image']) as opened:art=opened.convert('RGBA')
    native_w,native_h=item['native_size'];sx=size[0]/256;sy=size[1]/192
    art=art.resize((round(native_w*sx),round(native_h*sy)),Image.Resampling.LANCZOS)
    if owner and owner['name']!=item['name'] and owner.get('palette')!=item.get('palette'):
        # Shared geometry is painted once. Transfer the native palette's
        # spatial color change while preserving the painted high-frequency art.
        with Image.open(ROOT/'graphics'/owner['native']) as im:base=np.asarray(im.convert('RGB'),dtype='float32')
        with Image.open(ROOT/'graphics'/item['native']) as im:target=np.asarray(im.convert('RGB'),dtype='float32')
        if base.shape==target.shape:
            delta=target-base;pixels=np.array(art);colored=pixels[:,:,:3].astype('float32')
            for channel in range(3):
                field=Image.fromarray(delta[:,:,channel],mode='F').resize(art.size,Image.Resampling.BILINEAR)
                colored[:,:,channel]+=np.asarray(field)
            pixels[:,:,:3]=np.clip(np.rint(colored),0,255).astype('uint8');art=Image.fromarray(pixels)
    canvas=Image.new('RGBA',(round(hardware[0]*sx),round(hardware[1]*sy)));canvas.paste(art,(0,0))
    return canvas

class BattleBackgroundRenderer:
    def __init__(self,async_prepare=True):
        self.catalog_stamp=0;self.cached_rows=[];self.path=FOLDER/'catalog.json';self.index_path=FOLDER/'runtime_index/index.json';self.next_scan=0;self.index_stamp=0;self.generation=0
        self.sample_plans=OrderedDict();self.gpu_masks=OrderedDict();self.uv_corrections={};self.active_layers={};self.items={};self.by_name={};self.references=None;self.layer_indices={};self.pending={};self.errors={};self.art=OrderedDict();self.viewports=OrderedDict();self.identifications=OrderedDict();self.last_matches=[];self.matched_layers=set();self.last_rows=[];self.last_identification=[];self.last_ms=0
        self.executor=ThreadPoolExecutor(max_workers=1,thread_name_prefix='battle-BG-HD') if async_prepare else None

    def collect(self):
        for key,future in list(self.pending.items()):
            if not future.done():continue
            del self.pending[key]
            try:
                if key=='catalog':self.apply_assets(future.result())
                else:self.art[key]=future.result();self.generation+=1
            except Exception as error:self.errors[key]=str(error)
        while len(self.art)>2:self.art.popitem(last=False)

    def scan_assets(self):
        # Disk reads and JSON inflation stay on the preparation worker in play.
        if not self.path.exists() or not self.index_path.exists():return None
        catalog_stamp=self.path.stat().st_mtime_ns
        rows=self.cached_rows
        if catalog_stamp!=self.catalog_stamp:rows=json.loads(self.path.read_text(encoding='utf-8'))['resources']
        stamp=self.index_path.stat().st_mtime_ns;meta=None;references=None
        if stamp!=self.index_stamp:
            meta=json.loads(self.index_path.read_text());references=np.load(FOLDER/'runtime_index/references.npy',mmap_mode='r')
        by_name={row['name']:row for row in rows};stamps={}
        for path in {row['image'] for row in rows}:
            try:stamps[path]=(ROOT/'graphics'/path).stat().st_mtime_ns
            except OSError:pass
        ready={name:row for name,row in by_name.items() if row['image'] in stamps}
        signature=tuple(sorted((name,row['image'],stamps[row['image']],row.get('art_owner')) for name,row in ready.items()))
        return rows,catalog_stamp,stamp,meta,references,by_name,ready,signature

    def apply_assets(self,result):
        if result is None:return
        rows,catalog_stamp,stamp,meta,references,by_name,ready,signature=result
        self.cached_rows=rows;self.catalog_stamp=catalog_stamp
        if meta is not None:
            self.references=references;self.names=meta['names'];self.native_sizes=meta['sizes'];self.layer_indices={layer:np.array([i for i,ls in enumerate(meta['layers']) if layer in ls],dtype='int32') for layer in (2,3)};self.index_stamp=stamp;self.identifications.clear()
        if signature!=getattr(self,'asset_signature',None):
            self.asset_signature=signature;self.items=ready;self.by_name=by_name;self.identifications.clear();self.viewports.clear();self.art.clear();self.errors.clear();self.generation+=1

    def refresh(self):
        self.collect()
        now=time.monotonic()
        if now<self.next_scan:return
        self.next_scan=now+2
        if self.executor:
            if 'catalog' not in self.pending:self.pending['catalog']=self.executor.submit(self.scan_assets)
        else:
            try:self.apply_assets(self.scan_assets())
            except (OSError,ValueError,KeyError):return

    @staticmethod
    def battle_layers(bg_layout):
        if bg_layout is None or len(bg_layout)!=4:return []
        rows=[]
        for layer in (3,2):
            info=bg_layout[layer]
            if len(info)<9:continue
            cnt,_,_,x,y,w,h,visible,_=map(int,info[:9]);charbase=(cnt>>2)&15
            if visible and w in (256,512) and h in (256,512) and charbase==(6 if layer==3 else 4):rows.append((layer,x,y,w,h))
        return rows

    def identify(self,native,layer_ids,row,preferred=True):
        layer,x,y,w,h=row;sample_key=(self.current_ids_signature if hasattr(self,'current_ids_signature') else layer_ids.tobytes(),layer)
        try:plan=self.sample_plans.pop(sample_key)
        except KeyError:
            where=np.flatnonzero(layer_ids==layer)
            sample=where[::max(1,len(where)//96)][:128];plan=(sample//256,sample%256) if len(where)>=64 else None
        self.sample_plans[sample_key]=plan
        while len(self.sample_plans)>4:self.sample_plans.popitem(last=False)
        if plan is None:return None
        ys,xs=plan;sample=ys;pixels=native[ys,xs].astype('uint16')>>3;actual=pixels[:,0]|(pixels[:,1]<<5)|(pixels[:,2]<<10)
        if len(np.unique(actual))<3:return None
        previous=self.active_layers.get(layer) if preferred else None
        candidates=[previous] if previous is not None and self.names[previous] in self.items else self.layer_indices.get(layer,())
        candidates=np.array([int(i) for i in candidates if self.names[int(i)] in self.items],dtype='int32')
        if not len(candidates):return None
        # End-of-frame BG registers can be one pixel ahead of the displayed
        # raster. Validate nearby UVs rather than silently painting shifted art.
        offsets=((0,0),(1,-1),(-1,1),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1));last_offset=self.uv_corrections.get(layer,(0,0))
        for dx,dy in (last_offset,)+tuple(offset for offset in offsets if offset!=last_offset):
            rx=(xs+x+dx)%w;ry=(ys+y+dy)%h;coordinate=(rx<256)&(ry<256)
            expected=np.array(self.references[candidates[:,None],np.minimum(ry,255)[None,:],np.minimum(rx,255)[None,:]])
            valid=((expected&32768)!=0)&coordinate[None,:];counts=valid.sum(1);expected&=32767
            er=np.abs((expected&31).astype('int16')-(actual[None,:]&31).astype('int16'));eg=np.abs(((expected>>5)&31).astype('int16')-((actual[None,:]>>5)&31).astype('int16'));eb=np.abs(((expected>>10)&31).astype('int16')-((actual[None,:]>>10)&31).astype('int16'))
            exact=((expected==actual[None,:])&valid).sum(1);near=((er<=1)&(eg<=1)&(eb<=1)&valid).sum(1)
            eligible=(counts>=len(sample)*.75)&(near>=counts*.90)&(exact>=counts*.60)
            if eligible.any():
                scores=np.where(eligible,(exact+near)/np.maximum(counts,1),-1);best=int(candidates[int(np.argmax(scores))]);self.active_layers[layer]=best;self.uv_corrections[layer]=(dx,dy);return self.names[best],(layer,x+dx,y+dy,w,h)
        if previous is not None:return self.identify(native,layer_ids,row,preferred=False)
        return None

    def texture(self,name,size,hardware):
        item=self.items[name];key=(name,size,hardware,item['image']);value=self.art.pop(key,None)
        if value is not None:self.art[key]=value;return value
        if key in self.errors:return None
        owner=self.by_name.get(item.get('art_owner'))
        if self.executor:
            if key not in self.pending:self.pending[key]=self.executor.submit(prepare_texture,item,owner,size,hardware)
            return None
        value=prepare_texture(item,owner,size,hardware);self.art[key]=value
        while len(self.art)>2:self.art.popitem(last=False)
        return value

    def compose(self,image,native,layer_ids,bg_layout):
        start=time.perf_counter();self.last_matches=[];self.matched_layers=set();self.last_rows=[];self.last_identification=[];rows=self.battle_layers(bg_layout)
        if not rows:self.last_ms=(time.perf_counter()-start)*1000;return False
        self.refresh()
        if not rows or self.references is None or not self.items:self.last_ms=(time.perf_counter()-start)*1000;return False
        native=np.asarray(native,dtype='uint8')[:192];layer_ids=np.asarray(layer_ids,dtype='uint8');self.current_ids_signature=layer_ids.tobytes();signature=(zlib.crc32(native.tobytes()),self.current_ids_signature,tuple(rows),self.generation)
        try:matches=self.identifications.pop(signature)
        except KeyError:matches=[match for row in rows if (match:=self.identify(native,layer_ids,row)) is not None]
        self.identifications[signature]=matches
        while len(self.identifications)>2:self.identifications.popitem(last=False)
        for name,row in matches:
            self.last_identification.append(name);layer,x,y,w,h=row;art=self.texture(name,image.size,(w,h))
            if art is None:continue
            if hasattr(image,'draw'):
                extra=getattr(self,'hud_mask',None) if layer==3 else None
                mask_key=(self.current_ids_signature,layer,image.size,None if extra is None else extra.tobytes())
                mask=self.gpu_masks.pop(mask_key,None)
                if mask is None:mask=Image.fromarray(((layer_ids==layer) if extra is None else ((layer_ids==layer)|extra)).astype('uint8')*255).resize(image.size,Image.Resampling.NEAREST)
                self.gpu_masks[mask_key]=mask
                while len(self.gpu_masks)>2:self.gpu_masks.popitem(last=False)
                px=round((x%w)*image.width/256);py=round((y%h)*image.height/192)
                for dx in (-px,art.width-px):
                    for dy in (-py,art.height-py):
                        if dx<image.width and dy<image.height and dx+art.width>0 and dy+art.height>0:
                            image.draw(art,(dx,dy,dx+art.width,dy+art.height),mask=mask,mask_rect=(0,0,*image.size),alpha=True)
                self.last_matches.append(name);self.matched_layers.add(layer);self.last_rows.append((name,row));continue
            key=(name,x%w,y%h,w,h,image.size,self.generation);viewport=self.viewports.pop(key,None)
            if viewport is None:
                viewport=Image.new('RGBA',image.size);px=round((x%w)*image.width/256);py=round((y%h)*image.height/192)
                for dx in (-px,art.width-px):
                    for dy in (-py,art.height-py):
                        left=max(0,dx);top=max(0,dy);right=min(image.width,dx+art.width);bottom=min(image.height,dy+art.height)
                        if left<right and top<bottom:viewport.paste(art.crop((left-dx,top-dy,right-dx,bottom-dy)),(left,top))
            self.viewports[key]=viewport
            while len(self.viewports)>2:self.viewports.popitem(last=False)
            visible=layer_ids==layer
            if layer==3 and getattr(self,'hud_mask',None) is not None:visible=visible|self.hud_mask
            mask=Image.fromarray(visible.astype('uint8')*255).resize(image.size,Image.Resampling.NEAREST);alpha=np.asarray(mask,dtype='uint16')*np.asarray(viewport.getchannel('A'),dtype='uint16')//255
            image.paste(viewport,(0,0),Image.fromarray(alpha.astype('uint8')));self.last_matches.append(name);self.matched_layers.add(layer);self.last_rows.append((name,row))
        self.last_ms=(time.perf_counter()-start)*1000;return bool(self.last_matches)

    def close(self):
        if self.executor:self.executor.shutdown(wait=False,cancel_futures=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--compile',action='store_true');args=parser.parse_args()
    if args.compile:compile_native_index()
