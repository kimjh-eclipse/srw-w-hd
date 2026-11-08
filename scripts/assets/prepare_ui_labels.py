"""Register exact native ability-panel image lettering, without editing a ROM."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json
import numpy as np
from PIL import Image
ROOT=PROJECT_ROOT
OUT=ROOT/'graphics/fonts/ui_labels'

def prepare():
    OUT.mkdir(parents=True,exist_ok=True)
    source=ROOT/'test_current/font/scene_1.png'
    native=np.asarray(Image.open(source).convert('RGB'))[:192]
    records=[];arrays={}
    for name,text,box,color in [('hp','HP',(4,96,20,104),'yellow'),('en','EN',(4,112,20,120),'yellow'),('parts','PARTS',(96,112,128,120),'white')]:
        x,y,r,b=box;cell=native[y:b,x:r]
        mask=((cell[:,:,0]>190)&(cell[:,:,1]>140)&(cell[:,:,2]<100)) if color=='yellow' else cell.min(2)>=232
        arrays[name]=mask
        records.append(dict(name=name,text=text,box=box,color=color,ink_pixels=int(mask.sum())))
    gates=[]
    for i,box in enumerate([(64,16,88,28),(8,48,32,60),(8,64,32,76)]):
        x,y,r,b=box;arrays['gate'+str(i)]=native[y:b,x:r].min(2)>=232;gates.append(box)
    np.savez_compressed(OUT/'patterns.npz',**arrays)
    data=dict(source=str(source.relative_to(ROOT)),labels=records,ability_gates=gates,
              registration='Exact ink bitmaps at native layout positions; no OCR, static screen replacement, or numeric-value templates.',
              dynamic_glyphs='Owned by normal FontRenderer: existing verified CP949 12px, narrow 8x12 and HUD 8x8 ROM tables. No duplicate scan in this module.')
    (OUT/'library.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(data,ensure_ascii=False))

if __name__=='__main__':prepare()
