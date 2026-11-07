"""Exact map-cell recognition and coherent HD world sampling on either display.

Grid, units, selection overlays and menus retain their live native pixels.
Only pixels equal to the registered terrain at the inferred camera are replaced.
"""
import json,zlib,time,hashlib
from collections import Counter,OrderedDict
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

class MapTilesRenderer:
    def __init__(self):
        path=ROOT/'graphics/map_tiles/library.json';self.path=path;self.stamp=path.stat().st_mtime_ns if path.exists() else 0;self.checked=0;self.generation=0;self.pending={}
        self.specs=json.loads(path.read_text())['maps'] if path.exists() else []
        self.loaded=False;self.maps={};self.lookup={};self.overviews={};self.art_cache=OrderedDict();self.source_cache=OrderedDict();self.world_views=OrderedDict();self.overview_art=OrderedDict();self.last_matches=[];self.plans=OrderedDict();self.last_ms=0;self.last_background=None;self.compiled=None;self.overview_lookup={}

    def refresh(self):
        now=time.monotonic()
        if now-self.checked<2:return
        self.checked=now
        stamp=self.path.stat().st_mtime_ns if self.path.exists() else 0
        if stamp==self.stamp:return
        try:specs=json.loads(self.path.read_text())['maps'] if stamp else []
        except (OSError,ValueError):return
        old={r['id']:r.get('source_sha256') for r in self.specs};new={r['id']:r.get('source_sha256') for r in specs}
        if any(new.get(i)!=sha for i,sha in old.items()):self.maps.clear();self.lookup.clear()
        self.specs=specs;self.stamp=stamp;self.loaded=False;self.art_cache.clear();self.world_views.clear();self.overview_art.clear();self.plans.clear();self.generation+=1

    def load(self):
        if self.loaded:return
        if self.load_compiled():return
        folder=ROOT/'graphics/map_tiles'
        for spec in self.specs:
            if spec.get('overview_native') and spec['id'] not in self.overviews:
                w,h=spec['overview_size'];reference=np.asarray(Image.open(folder/spec['overview_native']).convert('RGB'))[:h,:w]>>3
                anchors=[]
                for y in range(0,h-7,16):
                    for x in range(0,w-7,16):
                        patch=reference[y:y+8,x:x+8];score=float(patch.astype('float32').std())
                        if len(np.unique(patch.reshape(-1,3),axis=0))>8:anchors.append((score,x,y,patch))
                self.overviews[spec['id']]=(reference,sorted(anchors,key=lambda a:a[0],reverse=True)[:6],spec)
            if spec['id'] in self.maps:
                self.maps[spec['id']]=(self.maps[spec['id']][0],spec);continue
            source=np.asarray(Image.open(folder/spec['native']).convert('RGB'))>>3
            self.maps[spec['id']]=(source,spec)
            h,w=source.shape[:2]
            for y in range(0,h-15,16):
                for x in range(0,w-15,16):
                    key=source[y+1:y+16,x+1:x+16].tobytes()
                    self.lookup.setdefault(key,[]).append((spec['id'],x,y))
        self.loaded=True

    def load_compiled(self):
        folder=ROOT/'graphics/map_tiles/runtime_index';path=folder/'index.json'
        if not path.exists():return False
        if self.compiled is None:
            self.compiled=json.loads(path.read_text())['maps'];self.index_keys=np.load(folder/'keys.npy',mmap_mode='r');self.index_offsets=np.load(folder/'offsets.npy',mmap_mode='r');self.index_coords=np.load(folder/'coordinates.npy',mmap_mode='r');self.index_overviews=np.load(folder/'overviews.npy',mmap_mode='r')
        if any(str(s['id']) not in self.compiled or self.compiled[str(s['id'])]['source_sha256']!=s['source_sha256'] for s in self.specs):return False
        self.maps={s['id']:(None,s) for s in self.specs};self.available=np.zeros(65536,dtype='bool');self.overviews={};self.overview_lookup={}
        for spec in self.specs:
            mid=spec['id'];self.available[mid]=True;meta=self.compiled[str(mid)];w,h=meta['overview_size'];reference=self.index_overviews[meta['overview_index'],:h,:w];anchors=[]
            for x,y in meta['anchors']:
                patch=reference[y:y+8,x:x+8];anchors.append((0,x,y,patch));self.overview_lookup.setdefault(patch.tobytes(),[]).append((mid,x,y))
            self.overviews[mid]=(reference,anchors,spec)
        self.loaded=True;return True

    def source(self,mid):
        source,spec=self.maps[mid]
        if source is not None:return source,spec
        source=self.source_cache.pop(mid,None)
        if source is None:source=np.load(ROOT/'graphics/map_tiles/runtime_index'/self.compiled[str(mid)]['source'],mmap_mode='r')
        self.source_cache[mid]=source
        while len(self.source_cache)>2:self.source_cache.popitem(last=False)
        return source,spec

    def overview_plan(self,native,size):
        if not any(r.get('overview_native') for r in self.specs):return None
        # Overview maps occupy the center of the teal tactical grid. Check
        # its unobscured side strips before any template/index work; animated
        # battle backdrops and cut-ins must not scan 114 minimap references.
        outer=np.concatenate((native[:128,:16],native[:128,-16:]),axis=1)
        red=outer[:,:,0];green=outer[:,:,1].astype('int16');blue=outer[:,:,2].astype('int16')
        grid=(red<12)&(np.abs(green-blue)<8)
        if np.count_nonzero(grid)<grid.size*.92 or np.count_nonzero(grid&(green>20))<grid.size*.02:return None
        self.load();q=native>>3;lines=[row.tobytes() for row in q];fast_candidates=Counter()
        if self.overview_lookup:
            for y in range(0,185,8):
                for x in range(0,249,8):
                    for mid,sx,sy in self.overview_lookup.get(q[y:y+8,x:x+8].tobytes(),()):fast_candidates[(mid,x-sx,y-sy)]+=1
        for mid,(reference,anchors,spec) in self.overviews.items():
            h,w=reference.shape[:2];candidates=Counter()
            if self.overview_lookup:
                candidates.update({(x,y):votes for (key,x,y),votes in fast_candidates.items() if key==mid})
            else:
                for _,sx,sy,patch in anchors:
                    needle=patch[0].tobytes()
                    for y in range(185):
                        line=lines[y];at=line.find(needle)
                        while at>=0:
                            x=at//3
                            if at%3==0 and x+8<=256 and np.array_equal(q[y:y+8,x:x+8],patch):candidates[(x-sx,y-sy)]+=1
                            at=line.find(needle,at+3)
            for (x,y),votes in candidates.most_common(3):
                if votes<2 or min(x,y)<0 or x+w>256 or y+h>192:continue
                visible=np.all(q[y:y+h,x:x+w]==reference,axis=2)
                if visible.mean()<.80:continue
                source,row=self.source(mid);art=self.art_cache.pop(mid,None)
                if art is None:art=Image.open(ROOT/'graphics/map_tiles'/row['image']).convert('RGB')
                self.art_cache[mid]=art
                while len(self.art_cache)>2:self.art_cache.popitem(last=False)
                left=round(x*size[0]/256);top=round(y*size[1]/192);right=round((x+w)*size[0]/256);bottom=round((y+h)*size[1]/192)
                cachekey=(mid,size,spec.get('image_sha256'));viewport=self.overview_art.pop(cachekey,None)
                if viewport is None:
                    l,t,r,b=spec['overview_crop'];sh,sw=source.shape[:2];viewport=art.crop((round(l*art.width/sw),round(t*art.height/sh),round(r*art.width/sw),round(b*art.height/sh))).resize((right-left,bottom-top),Image.Resampling.LANCZOS)
                self.overview_art[cachekey]=viewport
                while len(self.overview_art)>2:self.overview_art.popitem(last=False)
                mask=Image.fromarray(visible.astype('uint8')*255).resize(viewport.size,Image.Resampling.NEAREST)
                return [(viewport,(left,top),mask)],dict(map=mid,overview=True,position=[x,y],landmark_votes=votes,pixels=int(visible.sum())),None
        return None

    @staticmethod
    def phase(native):
        black=(native[:,:,0]<8)&(native[:,:,1]<8)&(native[:,:,2]<8)
        if np.count_nonzero(black)>black.size*.85:return None
        # A tactical grid has coherent vertical AND horizontal black lines.
        col=black[:128].sum(0);row=black.sum(1)
        xp=int(np.argmax(col.reshape(16,16).sum(0)));yp=int(np.argmax(row.reshape(12,16).sum(0)))
        if np.count_nonzero(col[xp::16]>=72)<10 or np.count_nonzero(row[yp::16]>=160)<5:return None
        return xp,yp

    def plan(self,native,size,gpu=False):
        phase=self.phase(native)
        if phase is None:return self.overview_plan(native,size)
        self.load();q=native>>3;xp,yp=phase;votes=Counter()
        for y in range(yp,177,16):
            for x in range(xp,241,16):
                sample=q[y+1:y+16,x+1:x+16].tobytes()
                if self.compiled is not None and self.overview_lookup:
                    key=int.from_bytes(hashlib.blake2b(sample,digest_size=8).digest(),'little');loc=int(np.searchsorted(self.index_keys,key))
                    if loc>=len(self.index_keys) or int(self.index_keys[loc])!=key:continue
                    start,length=map(int,self.index_offsets[loc]);coordinates=self.index_coords[start:start+length];found=coordinates[self.available[coordinates[:,0]]]
                else:found=self.lookup.get(sample,())
                # Uniform ocean/space cells have many equally valid locations;
                # landmarks alone establish the camera without quadratic work.
                if self.compiled is None and len(found)>8:continue
                for mid,sx,sy in found:votes[(int(mid),int(sx)-x,int(sy)-y)]+=1
        if not votes:return None
        (mid,dx,dy),count=votes.most_common(1)[0]
        if count<6:return None
        source,spec=self.source(mid);h,w=source.shape[:2]
        art=self.art_cache.pop(mid,None)
        if art is None:art=Image.open(ROOT/'graphics/map_tiles'/spec['image']).convert('RGB')
        self.art_cache[mid]=art
        while len(self.art_cache)>2:self.art_cache.popitem(last=False)
        yy=np.arange(192)+dy;xx=np.arange(256)+dx
        valid=(yy[:,None]>=0)&(yy[:,None]<h)&(xx[None,:]>=0)&(xx[None,:]<w)
        expected=source[np.clip(yy,0,h-1)][:,np.clip(xx,0,w-1)]
        mask=np.all(q==expected,axis=2)&valid
        # Exclude UI panels, even if a few of their colors equal map pixels.
        for y in range(yp-16,192,16):
            for x in range(xp-16,256,16):
                region=mask[max(0,y):min(192,y+16),max(0,x):min(256,x+16)]
                if np.count_nonzero(region)<region.size*.38:region[:]=False
        # A moving camera only crops a display-sized world texture. Repeating
        # Lanczos for every one-pixel scroll was far costlier than decoding it.
        viewkey=(mid,size,spec.get('image_sha256'));world=self.world_views.pop(viewkey,None);sx=size[0]/256;sy=size[1]/192
        if world is None:world=art.resize((round(w*sx),round(h*sy)),Image.Resampling.LANCZOS)
        self.world_views[viewkey]=world
        while len(self.world_views)>2:self.world_views.popitem(last=False)
        viewportkey=(viewkey,dx,dy)
        if not hasattr(self,'viewports'):self.viewports=OrderedDict()
        viewport=self.viewports.pop(viewportkey,None)
        if viewport is None:viewport=world.crop((round(dx*sx),round(dy*sy),round(dx*sx)+size[0],round(dy*sy)+size[1]))
        self.viewports[viewportkey]=viewport
        while len(self.viewports)>2:self.viewports.popitem(last=False)
        alpha=Image.fromarray(mask.astype('uint8')*255).resize(size,Image.Resampling.NEAREST)
        if gpu:return [(viewport,(0,0),alpha)],dict(map=mid,camera=[dx,dy],landmark_votes=count,pixels=int(mask.sum())),viewport
        patches=[]
        for y in range(yp-16,192,16):
            for x in range(xp-16,256,16):
                box=(round(max(0,x)*size[0]/256),round(max(0,y)*size[1]/192),round(min(256,x+16)*size[0]/256),round(min(192,y+16)*size[1]/192))
                patchmask=alpha.crop(box);bounds=patchmask.getbbox()
                if bounds is None:continue
                l,t,r,b=bounds;box=(box[0]+l,box[1]+t,box[0]+r,box[1]+b);patchmask=patchmask.crop(bounds)
                patches.append((viewport.crop(box),box[:2],None if patchmask.getextrema()==(255,255) else patchmask))
        return patches,dict(map=mid,camera=[dx,dy],landmark_votes=count,pixels=int(mask.sum())),viewport

    def compose(self,image,native):
        start=time.perf_counter();self.refresh();native=np.asarray(native,dtype='uint8')[:192];gpu=hasattr(image,'draw');key=(zlib.crc32(native.tobytes()),image.size,gpu)
        try:plan=self.plans.pop(key)
        except KeyError:plan=self.plan(native,image.size,gpu=gpu)
        self.plans[key]=plan
        while len(self.plans)>2:self.plans.popitem(last=False)
        self.last_matches=[];self.last_background=None
        if plan is not None:
            patches,info,self.last_background=plan
            for art,position,mask in patches:image.paste(art,position,mask)
            self.last_matches=[info]
        self.last_ms=(time.perf_counter()-start)*1000
        return bool(self.last_matches)

# Naming convenience for older callers.
MapRenderer=MapTilesRenderer
