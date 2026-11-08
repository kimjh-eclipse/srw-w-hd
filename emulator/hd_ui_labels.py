"""Exact ability-screen HP/EN/PARTS image lettering.

The three native layout anchors must all match before any pixel is altered.
Variable numbers remain owned by the normal ROM-table FontRenderer.
"""
from collections import OrderedDict
from pathlib import Path
import json,zlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont

from asset_paths import asset_root
ROOT=asset_root(Path(__file__).resolve().parent.parent)

class UILabelRenderer:
    def __init__(self):
        folder=ROOT/'graphics/fonts/ui_labels'
        self.library=json.loads((folder/'library.json').read_text(encoding='utf-8'))
        with np.load(folder/'patterns.npz') as f:self.patterns={k:f[k].copy() for k in f.files}
        self.last_matches=[];self.glyphs=OrderedDict();self.cache_key=None;self.cache=[]
        self.stamp=1

    @staticmethod
    def _mask(cell,color='white'):
        if color=='yellow':return (cell[:,:,0]>190)&(cell[:,:,1]>140)&(cell[:,:,2]<100)
        return cell.min(2)>=232

    def is_ability(self,native):
        if native.shape!=(192,256,3):return False
        for i,(x,y,r,b) in enumerate(self.library['ability_gates']):
            if not np.array_equal(self._mask(native[y:b,x:r]),self.patterns['gate'+str(i)]):return False
        return True

    def _text(self,text,size,color):
        key=(text,size,color)
        if key not in self.glyphs:
            w,h=size;font=ImageFont.truetype('C:/Windows/Fonts/malgun.ttf',max(8,round(h*.94)))
            im=Image.new('RGBA',size);draw=ImageDraw.Draw(im);box=draw.textbbox((0,0),text,font=font)
            draw.text(((w-box[2]+box[0])/2-box[0],(h-box[3]+box[1])/2-box[1]),text,font=font,fill=color,stroke_width=max(1,h//45),stroke_fill=(8,16,20,255))
            self.glyphs[key]=im
            while len(self.glyphs)>64:self.glyphs.popitem(last=False)
        return self.glyphs[key]

    def prewarm(self):
        from render_resolution import MIN_WIDTH,MAX_WIDTH
        for screen in range(MIN_WIDTH,MAX_WIDTH+1,32):
            scale=screen/256
            for row in self.library['labels']:
                x,y,r,b=row['box'];size=round(r*scale)-round(x*scale),round(b*scale)-round(y*scale)
                color=(255,232,0,255) if row['color']=='yellow' else (255,255,255,255)
                self._text(row['text'],size,color)

    def compose(self,target,native):
        native=np.asarray(native,dtype='uint8')[:192]
        self.last_matches=[]
        if not self.is_ability(native):return 0
        sx,sy=target.width/256,target.height/192
        key=(target.size,tuple(zlib.crc32(native[max(0,row['box'][1]-1):min(192,row['box'][3]+1),max(0,row['box'][0]-1):min(256,row['box'][2]+1)].tobytes()) for row in self.library['labels']))
        if key!=self.cache_key:
            patches=[];matches=[]
            for row in self.library['labels']:
                x,y,r,b=row['box'];mask=self.patterns[row['name']]
                if not np.array_equal(self._mask(native[y:b,x:r],row['color']),mask):continue
                # Repair only native glyph ink plus its one-pixel outline.
                left,top=max(0,x-1),max(0,y-1);right,bottom=min(256,r+1),min(192,b+1)
                local=np.zeros((bottom-top,right-left),bool);local[y-top:b-top,x-left:r-left]=mask
                padded=np.pad(local,1);expanded=np.logical_or.reduce([padded[dy:dy+local.shape[0],dx:dx+local.shape[1]] for dy in range(3) for dx in range(3)])
                healed=native[top:bottom,left:right].copy();coords=np.arange(healed.shape[1])
                for yy in np.flatnonzero(expanded.any(1)):
                    keep=~expanded[yy]
                    if keep.any():
                        for c in range(3):healed[yy,expanded[yy],c]=np.interp(coords[expanded[yy]],coords[keep],healed[yy,keep,c])
                box=(round(left*sx),round(top*sy),round(right*sx),round(bottom*sy))
                patch=Image.fromarray(healed).convert('RGBA').resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.NEAREST)
                alpha=Image.fromarray(expanded.astype('uint8')*255).resize(patch.size,Image.Resampling.NEAREST);patch.putalpha(alpha)
                width,height=round(r*sx)-round(x*sx),round(b*sy)-round(y*sy)
                color=(255,232,0,255) if row['color']=='yellow' else (255,255,255,255)
                patch.alpha_composite(self._text(row['text'],(width,height),color),(round(x*sx)-box[0],round(y*sy)-box[1]))
                patches.append((box[:2],patch));matches.append((x,y,row['text']))
            self.cache_key=key;self.cache=(patches,matches)
        patches,matches=self.cache
        for position,patch in patches:target.paste(patch,position,patch)
        self.last_matches=list(matches)
        return len(matches)
