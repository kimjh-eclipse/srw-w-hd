"""Registered full-layer art with native foreground and scrolling preserved."""
import json,zlib
from stage_cache import StageCache
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import os as _os
# SRWW_RENDER_SHORTCUTS=0 restores the earlier per-frame work for comparison.
SHORTCUTS=_os.environ.get('SRWW_RENDER_SHORTCUTS','1')!='0'
from PIL import Image
from pathlib import Path
from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)
SCALE=1440/256

def periodic_texture(image,vertical=False):
    """Feather repeat sampling at the texture boundary, keeping PNGs intact."""
    pixels=np.asarray(image,dtype='float32').copy();band=max(2,round(8*SCALE))
    target=(pixels[:,0]+pixels[:,-1])/2
    weight=np.linspace(1,0,band,dtype='float32')[None,:,None]
    pixels[:,:band]=pixels[:,:band]*(1-weight)+target[:,None,:]*weight
    pixels[:,-band:]=pixels[:,-band:]*(1-weight[:,::-1])+target[:,None,:]*weight[:,::-1]
    if vertical:
        target=(pixels[0]+pixels[-1])/2;weight=np.linspace(1,0,band,dtype='float32')[:,None,None]
        pixels[:band]=pixels[:band]*(1-weight)+target[None,:,:]*weight
        pixels[-band:]=pixels[-band:]*(1-weight[::-1])+target[None,:,:]*weight[::-1]
    return Image.fromarray(np.clip(np.rint(pixels),0,255).astype('uint8'))

def prepare_background(item,scale=None):
    scale=SCALE if scale is None else scale
    with Image.open(ROOT/'graphics'/item['image']) as opened:
        art=opened.convert('RGB')
    with Image.open(ROOT/'graphics'/item['native']) as opened:
        native=opened.convert('RGB')
    w,h=native.size
    art=art.resize((round(w*scale),round(h*scale)),Image.Resampling.LANCZOS)
    if item.get('periodic',item['name']!='tower'):
        art=periodic_texture(art,vertical=item['name']=='space')
    return art,np.asarray(native)


class BackgroundRenderer:
    def __init__(self,async_prepare=False):
        self.items=StageCache();self.last_matches=[];self.pending={};self.prepare_errors={};self.mask_plans=OrderedDict();self.viewports=OrderedDict()
        path=ROOT/'graphics/backgrounds/library.json'
        self.specs={item['id']:item for item in json.loads(path.read_text())['backgrounds']} if path.exists() else {}
        self.executor=ThreadPoolExecutor(max_workers=1,thread_name_prefix='background-HD') if async_prepare else None

    def _art(self,bid):
        for key,future in list(self.pending.items()):
            if not future.done():continue
            del self.pending[key]
            try:self.items[key]=future.result()
            except Exception as error:self.prepare_errors[key]=str(error)
        cachekey=(bid,round(SCALE*256))
        if cachekey in self.items:
            value=self.items.pop(cachekey);self.items[cachekey]=value;return value
        if bid not in self.specs or cachekey in self.prepare_errors:return None
        if self.executor is not None:
            if cachekey not in self.pending:self.pending[cachekey]=self.executor.submit(prepare_background,self.specs[bid],SCALE)
            return None
        value=prepare_background(self.specs[bid],SCALE);self.items[cachekey]=value
        while len(self.items)>4:self.items.popitem(last=False)
        return value

    def close(self):
        if self.executor is not None:self.executor.shutdown(wait=False,cancel_futures=True)

    @staticmethod
    def _rectangles(grid):
        rectangles=[];active={}
        for y,row in enumerate(grid):
            padded=np.pad(row.astype('int8'),1);changes=np.flatnonzero(np.diff(padded));current={}
            for left,right in zip(changes[::2],changes[1::2]):
                key=(int(left),int(right))
                if key in active:
                    index=active[key];rectangles[index][3]=y+1
                else:
                    index=len(rectangles);rectangles.append([int(left),y,int(right),y+1])
                current[key]=index
            active=current
        return [(l*8,t*8,r*8,b*8) for l,t,r,b in rectangles]

    def _mask_plan(self,visible):
        key=visible.tobytes();result=self.mask_plans.pop(key,None)
        if result is None:
            blocks=visible.reshape(24,8,32,8);full=blocks.all((1,3));edges=blocks.any((1,3))&~full
            result=(self._rectangles(full),self._rectangles(edges))
        self.mask_plans[key]=result
        while len(self.mask_plans)>16:self.mask_plans.popitem(last=False)
        return result

    def compose(self,top,native,layer_ids,rows):
        self.last_matches=[]
        if rows is None:return
        for bid,x,y,layer in rows:
            prepared=self._art(bid)
            if prepared is None:continue
            while len(self.items)>4:self.items.popitem(last=False)
            art,source=prepared;h,w=source.shape[:2];x%=w;y%=h
            visible=layer_ids==layer
            if np.count_nonzero(visible)<32:continue
            expected=source[(np.arange(192)+y)%h][:,(np.arange(256)+x)%w]
            sample=np.flatnonzero(visible)[::max(1,np.count_nonzero(visible)//96)]
            error=np.median(np.abs(native[:192].reshape(-1,3)[sample].astype('int16')-expected.reshape(-1,3)[sample].astype('int16')).mean(axis=1))
            if error>5:continue
            if layer==getattr(self,'restoration_layer',None) and getattr(self,'restoration_mask',None) is not None:visible=visible|self.restoration_mask
            if layer==3 and getattr(self,'hud_mask',None) is not None:visible=visible|self.hud_mask
            if getattr(self,'window',None) is not None:visible=visible&(((self.window>>layer)&1)!=0)
            if hasattr(top,'draw'):
                if SHORTCUTS:
                    masks=self.__dict__.setdefault('native_masks',{});mask_key=(layer,visible.tobytes());mask=masks.get(mask_key)
                    if mask is None:
                        if len(masks)>8:masks.clear()
                        mask=masks[mask_key]=Image.fromarray(visible.astype('uint8')*255)
                else:mask=Image.fromarray(visible.astype('uint8')*255).resize(top.size,Image.Resampling.NEAREST)
                px,py=round(x*SCALE),round(y*SCALE)
                for dx in (-px,art.width-px):
                    for dy in (-py,art.height-py):
                        if dx<top.width and dy<top.height and dx+art.width>0 and dy+art.height>0:
                            top.draw(art,(dx,dy,dx+art.width,dy+art.height),mask=mask,mask_rect=(0,0,*top.size))
                self.last_matches.append(bid)
                continue
            key=(bid,x,y);viewport=self.viewports.pop(key,None)
            if viewport is None:
                viewport=Image.new('RGB',top.size);px=round(x*SCALE);py=round(y*SCALE)
                for dx in (-px,art.width-px):
                    for dy in (-py,art.height-py):
                        l=max(0,dx);u=max(0,dy);r=min(top.width,dx+art.width);b=min(top.height,dy+art.height)
                        if l<r and u<b:viewport.paste(art.crop((l-dx,u-dy,r-dx,b-dy)),(l,u))
            self.viewports[key]=viewport
            while len(self.viewports)>2:self.viewports.popitem(last=False)
            # Resize the whole visibility mask on one pixel grid. Resizing
            # separate tile-edge rectangles changes nearest-neighbor ties at
            # fractional scales and leaves native-color specks at boundaries.
            mask=Image.fromarray(visible.astype('uint8')*255).resize(top.size,Image.Resampling.NEAREST)
            box=mask.getbbox()
            if box is not None:top.paste(viewport.crop(box),box[:2],mask.crop(box))
            self.last_matches.append(bid)


def signature(tiles,maps):return [zlib.crc32(tiles),zlib.crc32(maps)]
