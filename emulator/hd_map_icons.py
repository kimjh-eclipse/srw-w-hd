"""Exact native map-icon identities; tiny lazy HD textures for either display."""
import json,time,zlib
from collections import OrderedDict,Counter
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent

class MapIconRenderer:
    def __init__(self):
        self.folder=ROOT/'graphics/map_icons';self.stamp=None;self.next_check=0.;self.records={};self.entries=[];self.lookup={};self.keys=np.array([],dtype='uint64');self.art=OrderedDict();self.cache=OrderedDict();self.healed=OrderedDict();self.pending={};self.last_matches=[];self.prepare_errors={};self.refresh()

    @staticmethod
    def codes(rgb):
        a=np.asarray(rgb,dtype='uint16')>>3
        return a[:,:,0]|(a[:,:,1]<<5)|(a[:,:,2]<<10)

    def refresh(self):
        now=time.monotonic()
        if now<self.next_check:return
        self.next_check=now+2;path=self.folder/'library.json';idxpath=self.folder/'native_indices.npz'
        if not path.exists() or not idxpath.exists():return
        stamp=(path.stat().st_mtime_ns,idxpath.stat().st_mtime_ns)
        if stamp==self.stamp:return
        meta=json.loads(path.read_text());self.palettes={int(k):np.array(v,dtype='uint16')[:,:3] for k,v in meta['palettes'].items()};self.records={r['resource']:r for r in meta['records'] if r.get('prepared')}
        data=np.load(idxpath);self.indices={int(k):a for k,a in zip(data['resources'],data['indices'])};self.entries=[];self.lookup={};frequencies=Counter()
        for idx in self.indices.values():
            for flip in range(4):
                source=idx[::-1] if flip&2 else idx
                if flip&1:source=source[:,::-1]
                valid=(source[:,:-3]>0)&(source[:,1:-2]>0)&(source[:,2:-1]>0)&(source[:,3:]>0)
                ys,xs=np.where(valid);runs=source[ys,xs].astype('uint32')|(source[ys,xs+1].astype('uint32')<<4)|(source[ys,xs+2].astype('uint32')<<8)|(source[ys,xs+3].astype('uint32')<<12)
                frequencies.update(set(map(int,runs)))
        for resource,idx in self.indices.items():
            if resource not in self.records:continue
            for flip in range(4):
                pixels=idx[::-1] if flip&2 else idx
                if flip&1:pixels=pixels[:,::-1]
                valid=(pixels[:,:-3]>0)&(pixels[:,1:-2]>0)&(pixels[:,2:-1]>0)&(pixels[:,3:]>0)
                ys,xs=np.where(valid)
                if not len(xs):continue
                runs=pixels[ys,xs].astype('uint32')|(pixels[ys,xs+1].astype('uint32')<<4)|(pixels[ys,xs+2].astype('uint32')<<8)|(pixels[ys,xs+3].astype('uint32')<<12)
                score=-4*np.log1p([frequencies[int(v)] for v in runs])-.1*((xs+1.5-7.5)**2+(ys-7.5)**2);pick=int(np.argmax(score));ax=int(xs[pick]);ay=int(ys[pick]);mask=pixels>0;yy,xx=np.where(mask)
                for palette,colors in self.palettes.items():
                    packed=(colors[:,0]>>3)|((colors[:,1]>>3)<<5)|((colors[:,2]>>3)<<10);expected=packed[pixels];run=expected[ay,ax:ax+4];key=sum(int(v)<<(16*j) for j,v in enumerate(run))
                    entry=dict(resource=resource,palette=palette,flip=flip,ax=ax,ay=ay,ys=yy,xs=xx,expected=expected[mask],mask=mask)
                    self.lookup.setdefault(key,[]).append(len(self.entries));self.entries.append(entry)
        self.keys=np.array(sorted(self.lookup),dtype='uint64');self.stamp=stamp;self.art.clear();self.cache.clear();self.healed.clear()

    def recognize(self,native):
        self.refresh();self.last_matches=[]
        if not len(self.keys):return []
        rgb=np.asarray(native)[:192,:256,:3];key=zlib.crc32(rgb.tobytes());cached=self.cache.pop(key,None)
        if cached is not None:self.cache[key]=cached;return cached
        code=self.codes(rgb);cursor_pixels=np.isin(code,[1057,32767,1016,992,768,640,512]);a=code.astype('uint64');packed=a[:,:-3]|(a[:,1:-2]<<16)|(a[:,2:-1]<<32)|(a[:,3:]<<48)
        positions=np.searchsorted(self.keys,packed);inside=positions<len(self.keys);positions=np.minimum(positions,len(self.keys)-1);candidate=inside&(self.keys[positions]==packed);found={}
        for ry,rx in zip(*np.where(candidate)):
            for index in self.lookup[int(packed[ry,rx])]:
                entry=self.entries[index];x=int(rx)-entry['ax'];y=int(ry)-entry['ay']
                if x<0 or y<0 or x+16>256 or y+16>192:continue
                actual=code[y+entry['ys'],x+entry['xs']];equal=actual==entry['expected']
                # The animated selection cursor is drawn over icon corners.
                # Its exact green/white/shadow colors are separate from the
                # five icon palettes; only those known overlay texels may
                # occlude a source match, with >=70% of ink still exact.
                cursor=cursor_pixels[y+entry['ys'],x+entry['xs']]
                if not equal.all() and not (equal.mean()>=.70 and np.all(equal|cursor)):continue
                old=found.get((x,y))
                if old is None or len(entry['xs'])>len(self.entries[old]['xs']):found[x,y]=index
        result=[dict(x=x,y=y,entry=index,resource=self.entries[index]['resource'],palette=self.entries[index]['palette'],flip=self.entries[index]['flip']) for (x,y),index in sorted(found.items())]
        self.cache[key]=result
        while len(self.cache)>8:self.cache.popitem(last=False)
        return result

    def texture(self,resource,palette,flip,size):
        key=(resource,palette,flip,size);found=self.art.pop(key,None)
        if found is not None:self.art[key]=found;return found
        record=self.records[resource];path=self.folder/record['prepared']
        with Image.open(path) as image:art=image.convert('RGBA')
        if palette!=3938:
            pixels=np.array(art);rgb=pixels[:,:,:3].astype('int16');source=self.palettes[3938].astype('int16');target=self.palettes[palette].astype('int16')
            nearest=np.argmin(((rgb.astype('float32')[:,:,None,:]-source[None,None,:,:])**2).sum(-1),axis=2)
            pixels[:,:,:3]=np.clip(rgb+target[nearest]-source[nearest],0,255).astype('uint8');art=Image.fromarray(pixels)
        if flip&1:art=art.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if flip&2:art=art.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if art.size!=(size,size):art=art.resize((size,size),Image.Resampling.LANCZOS)
        self.art[key]=art
        while len(self.art)>64:self.art.popitem(last=False)
        return art

    @staticmethod
    def healed_patch(native,x,y,mask):
        # Reconstruct only old opaque sprite texels from nearby uncovered map
        # pixels. A supplied clean HD background is preferable when available.
        source=np.asarray(native)[y:y+16,x:x+16,:3].astype('float32').copy();known=~mask
        for _ in range(16):
            if known.all():break
            total=np.zeros_like(source);count=np.zeros((16,16),dtype='float32')
            for sy,sx in ((0,1),(0,-1),(1,0),(-1,0)):
                k=np.roll(known,(sy,sx),(0,1));p=np.roll(source,(sy,sx),(0,1))
                if sy==1:k[0]=False
                if sy==-1:k[-1]=False
                if sx==1:k[:,0]=False
                if sx==-1:k[:,-1]=False
                total+=p*k[:,:,None];count+=k
            fill=(~known)&(count>0);source[fill]=total[fill]/count[fill,None];known|=fill
        return Image.fromarray(np.clip(source,0,255).astype('uint8'))

    def compose(self,target,native,background=None):
        matches=self.recognize(native);self.last_matches=matches
        scale=target.width/256;size=round(16*scale)
        for match in matches:
            x=match['x'];y=match['y'];entry=self.entries[match['entry']];box=(round(x*scale),round(y*scale),round(x*scale)+size,round(y*scale)+size)
            try:art=self.texture(match['resource'],match['palette'],match['flip'],size)
            except Exception as error:self.prepare_errors[str(match['resource'])]=str(error);continue
            original=np.asarray(native)[y:y+16,x:x+16,:3]
            if background is not None:
                patch=background.crop(box)
            else:
                heal_key=(zlib.crc32(original.tobytes()),match['resource'],match['flip'],size);patch=self.healed.pop(heal_key,None)
                if patch is None:patch=self.healed_patch(native,x,y,entry['mask']).resize((size,size),Image.Resampling.BILINEAR)
                self.healed[heal_key]=patch
                while len(self.healed)>64:self.healed.popitem(last=False)
            # Replace old opaque sprite pixels, retaining external selection
            # arrows and cell markers, then draw the smooth painted alpha.
            erase=Image.fromarray(entry['mask'].astype('uint8')*255).resize((size,size),Image.Resampling.NEAREST)
            target.paste(patch,box[:2],erase);target.paste(art,box[:2],art)
            # Selection corners are drawn above the native icon. Restore
            # their exact overlay colors above the replacement as well.
            cursor=np.isin(self.codes(original),[1057,32767,1016,992,768,640,512])
            if cursor.any():
                overlay=Image.fromarray(original).resize((size,size),Image.Resampling.NEAREST);mask=Image.fromarray(cursor.astype('uint8')*255).resize((size,size),Image.Resampling.NEAREST);target.paste(overlay,box[:2],mask)
        return len(matches)

    def close(self):self.art.clear();self.cache.clear();self.healed.clear()
