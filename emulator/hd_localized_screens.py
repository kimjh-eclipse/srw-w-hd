"""Exact native-image signatures select HD Korean chapter screens."""
import json,hashlib,time
from pathlib import Path
from collections import OrderedDict
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)

class LocalizedScreens:
    def __init__(self):
        self.path=ROOT/'graphics/localized_screens/chapter_library.json';self.checked=0;self.stamp=-1;self.generation=0;self.pending={};self.items={};self.images=OrderedDict();self.last_match=None;self.refresh()

    def refresh(self):
        now=time.monotonic()
        if now-self.checked<2:return
        self.checked=now;credits=self.path.with_name('copyright_library.json')
        stamp=(self.path.stat().st_mtime_ns if self.path.exists() else 0,credits.stat().st_mtime_ns if credits.exists() else 0)
        if stamp==self.stamp:return
        try:
            meta=json.loads(self.path.read_text(encoding='utf-8')) if stamp[0] else dict(titles=[])
            if stamp[1]:meta['titles'].extend(json.loads(credits.read_text(encoding='utf-8'))['screens'])
        except (ValueError,OSError):return
        self.items={r['ink_sha256']:r for r in meta['titles'] if r.get('image') or r.get('lines')};self.images.clear();self.stamp=stamp;self.generation+=1

    def stage_key(self,native):
        self.refresh()
        a=np.asarray(native,dtype='uint8')[:192];ink=(a[:,:,0]>210)&(a[:,:,1]>210)&(a[:,:,2]>210)
        row=self.items.get(hashlib.sha256(np.packbits(ink).tobytes()).hexdigest())
        return row.get('episode') if row is not None else None

    def compose(self,image,native):
        self.refresh();self.last_match=None
        if not self.items:return False
        a=np.asarray(native,dtype='uint8')[:192];ink=(a[:,:,0]>210)&(a[:,:,1]>210)&(a[:,:,2]>210)
        key=hashlib.sha256(np.packbits(ink).tobytes()).hexdigest();row=self.items.get(key)
        if row is None:return False
        # The exact full-screen white-ink mask identifies both the chapter
        # number and title; ordinary game dialogue cannot trigger this path.
        cachekey=(row['index'],image.size);art=self.images.pop(cachekey,None)
        if art is None:
            if row.get('lines'):
                art=Image.new('RGB',image.size);draw=ImageDraw.Draw(art)
                for number,line in enumerate(row['lines']):
                    point=round(image.height*9.5/192)
                    while True:
                        font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',point);box=draw.textbbox((0,0),line,font=font)
                        if box[2]-box[0]<image.width*.96 or point<12:break
                        point-=1
                    center=(9+24*number)*image.height/192
                    draw.text(((image.width-box[2]+box[0])/2,center-(box[1]+box[3])/2),line,font=font,fill='white')
            else:
                art=Image.open(ROOT/'graphics/localized_screens'/row['image']).convert('RGB')
                if art.size!=image.size:art=art.resize(image.size,Image.Resampling.LANCZOS)
        self.images[cachekey]=art
        while len(self.images)>2:self.images.popitem(last=False)
        image.paste(art,(0,0));self.last_match=row['index'];return True

ChapterRenderer=LocalizedScreens
