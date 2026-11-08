"""Pack directly observed missing textures, preserving native part boundaries."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,math
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=PROJECT_ROOT;FOLDER=ROOT/'test_current/attract/observed_parts';OUT=ROOT/'graphics/observed_parts';OUT.mkdir(exist_ok=True)
records=json.loads((FOLDER/'remaining.json').read_text());groups={}
for r in records:groups.setdefault(r['index_hash'],[]).append(r)
items=[]
for key,group in groups.items():
    r=max(group,key=lambda r:float(np.std(r['palette_rgb'])));im=Image.open(FOLDER/f"{r['hash']:08x}.png").convert('RGBA');a=np.asarray(im)
    if np.count_nonzero(a[:,:,3])<16 or len(np.unique(a[a[:,:,3]>0,:3],axis=0))<3:continue
    items.append((r,group,im))
canvas=Image.new('RGBA',(256,256));x=y=4;row=0;segments=[];sheets=[]
def flush():
    global canvas,x,y,row,segments
    if not segments:return
    name=f'observed_{len(sheets):03}';canvas.save(OUT/f'{name}_native.png');canvas.resize((2048,2048),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    sheets.append(dict(name=name,native_size=[256,256],segments=segments));canvas=Image.new('RGBA',(256,256));x=y=4;row=0;segments=[]
for r,group,im in sorted(items,key=lambda item:(item[0]['first']//1500,-item[2].height,-item[2].width)):
    w,h=im.size
    if x+w+4>256:x=4;y+=row+8;row=0
    if y+h+4>256:flush()
    canvas.paste(im,(x,y));segments.append(dict(x=x,y=y,w=w,h=h,source=r,variants=group));x+=w+8;row=max(row,h)
flush();(OUT/'sheets.json').write_text(json.dumps(dict(sheets=sheets,patterns=len(items)),indent=2))
contact=Image.new('RGB',(1024,math.ceil(len(sheets)/4)*280),'#17202b');d=ImageDraw.Draw(contact)
for i,s in enumerate(sheets):
    im=Image.open(OUT/(s['name']+'_native.png'));px=i%4*256;py=i//4*280;contact.paste(im,(px,py),im);d.text((px+4,py+256),f"{s['name']} : {len(s['segments'])}",fill='white')
contact.save(OUT/'review.png');print(len(items),len(sheets))
