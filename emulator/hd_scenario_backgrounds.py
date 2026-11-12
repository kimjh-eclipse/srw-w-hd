"""Exact source-pixel identification of ROM scenario backgrounds on either screen.

Only generated project assets participate. Text, portraits, markers and other
pixels that do not equal the original background remain owned by the game.
"""
import json,time,zlib
from stage_cache import StageCache
from collections import Counter,OrderedDict,defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import os as _os
# SRWW_RENDER_SHORTCUTS=0 restores the earlier per-frame work for comparison.
SHORTCUTS=_os.environ.get('SRWW_RENDER_SHORTCUTS','1')!='0'
from PIL import Image

from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)
SCALE=1440/256

def rgb555(rgb):
    q=np.asarray(rgb,dtype='uint16')>>3
    return q[:,:,0]|q[:,:,1]<<5|q[:,:,2]<<10

class ScenarioBackgrounds:
    def __init__(self,async_prepare=True):
        self.path=ROOT/'graphics/scenario_backgrounds/catalog.json'
        self.sources={};self.index=defaultdict(list);self.art=StageCache();self.pending={};self.errors={}
        self.executor=ThreadPoolExecutor(max_workers=1,thread_name_prefix='scenario-HD') if async_prepare else None
        self.next_scan=0.;self.last_match=None;self.cache=OrderedDict();self.generation=0
        self.native_cache=None
        self.catalog_stamp=None;self.catalog_items=[];self.asset_paths={}

    def load_native_cache(self):
        if self.native_cache is not None:return
        self.native_cache={};path=ROOT/'graphics/scenario_backgrounds/runtime_index.npz'
        if not path.exists():return
        with np.load(path,allow_pickle=False) as archive:
            names=archive['names'];heights=archive['heights'];references=archive['references'];keys=archive['keys'];xs=archive['xs'];ys=archive['ys'];resources=archive['resources']
        for index,name in enumerate(names):
            selected=np.flatnonzero(resources==index)
            anchors=[(int(xs[i]),int(keys[i]),int(ys[i])) for i in selected]
            self.native_cache[str(name)]=(references[index,:int(heights[index])],anchors)

    def refresh(self):
        now=time.monotonic()
        if now<self.next_scan:return
        self.next_scan=now+2
        if not self.path.exists():return
        try:
            stamp=self.path.stat().st_mtime_ns
            if stamp!=self.catalog_stamp:
                self.catalog_items=json.loads(self.path.read_text(encoding='utf-8'))['resources'];self.catalog_stamp=stamp
            items=self.catalog_items
        except (OSError,ValueError,KeyError):return
        for item in items:
            name=item['name']
            if name in self.sources:continue
            path=self.asset_paths.get(name)
            if path is None:path=ROOT/'graphics'/item['image'];self.asset_paths[name]=path
            if not path.exists():continue
            try:
                self.load_native_cache();cached=self.native_cache.get(name)
                if cached:
                    quantized,anchors=cached;h,w=quantized.shape
                else:
                    with Image.open(ROOT/'graphics'/item['native']) as opened:reference=np.asarray(opened.convert('RGB')).copy()
                    quantized=rgb555(reference);h,w=quantized.shape;anchors=[]
                    for x in (16,64,112,160,208):
                        for y in range(0,h-7,8):
                            patch=quantized[y:y+8,x:x+8]
                            if np.unique(patch).size>=4:anchors.append((x,zlib.crc32(patch.tobytes()),y))
                with Image.open(path) as opened:
                    if opened.width<w*2:continue
                if w!=256 or h<64:continue
                self.sources[name]=(item,quantized)
                for x,key,y in anchors:self.index[x,key].append((name,y))
                self.generation+=1
            except (OSError,ValueError) as error:self.errors[name]=str(error)

    def prepare(self,name,scale=None):
        scale=SCALE if scale is None else scale
        item,reference=self.sources[name];h,w=reference.shape
        with Image.open(ROOT/'graphics'/item['image']) as opened:
            return opened.convert('RGB').resize((round(w*scale),round(h*scale)),Image.Resampling.LANCZOS)

    def texture(self,name):
        for key,future in list(self.pending.items()):
            if not future.done():continue
            del self.pending[key]
            try:self.art[key]=future.result();self.generation+=1
            except Exception as error:self.errors[key]=str(error)
        cachekey=(name,round(SCALE*256))
        if cachekey in self.art:
            image=self.art.pop(cachekey);self.art[cachekey]=image;return image
        if cachekey in self.errors:return None
        if self.executor:
            if cachekey not in self.pending:self.pending[cachekey]=self.executor.submit(self.prepare,name,SCALE)
            return None
        self.art[cachekey]=self.prepare(name,SCALE);return self.art[cachekey]

    def compose(self,target,native):
        self.last_match=None;self.refresh()
        if not self.sources:return False
        source=np.asarray(native)[:192];q=rgb555(source)
        signature=(zlib.crc32(q.tobytes()),self.generation)
        cached=self.cache.pop(signature,None)
        if cached is None:
            votes=Counter()
            for y in range(32,161,16):
                for x in (16,64,112,160,208):
                    for name,sy in self.index.get((x,zlib.crc32(q[y:y+8,x:x+8].tobytes())),()):votes[name,sy-y]+=1
            cached=False
            for (name,dy),count in votes.most_common(4):
                if count<3:break
                reference=self.sources[name][1];h,w=reference.shape
                upper=max(0,-dy);lower=min(192,h-dy)
                if lower<=upper:continue
                mask=np.zeros((192,256),dtype='uint8')
                mask[upper:lower]=(q[upper:lower]==reference[upper+dy:lower+dy])*255
                if np.count_nonzero(mask)<2500:continue
                cached=(name,dy,mask);break
        self.cache[signature]=cached
        while len(self.cache)>4:self.cache.popitem(last=False)
        if cached is False:return False
        name,dy,mask=cached;art=self.texture(name)
        if art is None:return False
        if SHORTCUTS and hasattr(target,'draw'):
            # Same picture as the full-screen copy below (black where the art
            # does not reach), drawn from the cached art and the native mask.
            if getattr(self,'mask_source',None) is not mask:self.mask_source=mask;self.mask_image=Image.fromarray(mask)
            if not hasattr(self,'black'):self.black=Image.new('RGB',(1,1))
            upper=round(-dy*SCALE);full=(0,0,*target.size)
            target.draw(self.black,full,mask=self.mask_image,mask_rect=full)
            target.draw(art,(0,upper,art.width,upper+art.height),mask=self.mask_image,mask_rect=full)
            self.last_match=dict(name=name,source_offset_y=dy,replaced_pixels=int(np.count_nonzero(mask)))
            while len(self.art)>2:self.art.popitem(last=False)
            return True
        viewport=Image.new('RGB',target.size);viewport.paste(art,(0,round(-dy*SCALE)))
        target.paste(viewport,(0,0),Image.fromarray(mask).resize(target.size,Image.Resampling.NEAREST))
        self.last_match=dict(name=name,source_offset_y=dy,replaced_pixels=int(np.count_nonzero(mask)))
        while len(self.art)>2:self.art.popitem(last=False)
        return True

    def close(self):
        if self.executor:self.executor.shutdown(wait=False,cancel_futures=True)
