"""Registered full-layer art with native foreground and scrolling preserved."""
import json,zlib
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
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

def prepare_background(item):
    with Image.open(ROOT/'graphics'/item['image']) as opened:
        art=opened.convert('RGB')
    with Image.open(ROOT/'graphics'/item['native']) as opened:
        native=opened.convert('RGB')
    w,h=native.size
    art=art.resize((round(w*SCALE),round(h*SCALE)),Image.Resampling.LANCZOS)
    if item.get('periodic',item['name']!='tower'):
        art=periodic_texture(art,vertical=item['name']=='space')
    return art,np.asarray(native)


class BackgroundRenderer:
    def __init__(self,async_prepare=False):
        self.items=OrderedDict();self.last_matches=[];self.pending={};self.prepare_errors={}
        path=ROOT/'graphics/backgrounds/library.json'
        self.specs={item['id']:item for item in json.loads(path.read_text())['backgrounds']} if path.exists() else {}
        self.executor=ThreadPoolExecutor(max_workers=1,thread_name_prefix='background-HD') if async_prepare else None

    def _art(self,bid):
        for key,future in list(self.pending.items()):
            if not future.done():continue
            del self.pending[key]
            try:self.items[key]=future.result()
            except Exception as error:self.prepare_errors[key]=str(error)
        if bid in self.items:
            value=self.items.pop(bid);self.items[bid]=value;return value
        if bid not in self.specs or bid in self.prepare_errors:return None
        if self.executor is not None:
            if bid not in self.pending:self.pending[bid]=self.executor.submit(prepare_background,self.specs[bid])
            return None
        value=prepare_background(self.specs[bid]);self.items[bid]=value
        while len(self.items)>4:self.items.popitem(last=False)
        return value

    def close(self):
        if self.executor is not None:self.executor.shutdown(wait=False,cancel_futures=True)

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
            # Do not replace a differently colored palette, fade or alpha effect.
            sample=np.flatnonzero(visible)[::max(1,np.count_nonzero(visible)//96)]
            error=np.median(np.abs(native[:192].reshape(-1,3)[sample].astype('int16')-expected.reshape(-1,3)[sample].astype('int16')).mean(axis=1))
            if error>5:continue
            bounds=Image.fromarray(visible.astype('uint8')*255).getbbox()
            left,upper,right,lower=[round(v*SCALE) for v in bounds]
            mask=Image.fromarray(visible[bounds[1]:bounds[3],bounds[0]:bounds[2]].astype('uint8')*255).resize((right-left,lower-upper),Image.Resampling.NEAREST)
            px=round(x*SCALE);py=round(y*SCALE)
            for dx in (-px,art.width-px):
                for dy in (-py,art.height-py):
                    l=max(left,dx);u=max(upper,dy);r=min(right,dx+art.width);b=min(lower,dy+art.height)
                    if l>=r or u>=b:continue
                    top.paste(art.crop((l-dx,u-dy,r-dx,b-dy)),(l,u),mask.crop((l-left,u-upper,r-left,b-upper)))
            self.last_matches.append(bid)

def signature(tiles,maps):return [zlib.crc32(tiles),zlib.crc32(maps)]
