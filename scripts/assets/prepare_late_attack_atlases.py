"""Pack visually reviewed late battle mecha atlases, preserving source UVs."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
from functools import lru_cache
import sys,json,hashlib
import numpy as np
from PIL import Image
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=128)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
audit=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text())
palettes={i:p['palette'] for p in audit['patterns'] for i in p['image_group']}
review=json.loads((OUT/'scope_review.json').read_text())
ids=[p['image'] for p in review['items'] if p['classification']=='mechanical_or_attached_effect' and p['image']>20500]
items=[];duplicates={};seen={}
for i in ids:
    a=g.pixels(resource(i));digest=hashlib.sha256(a.tobytes()+bytes(str(a.shape),'ascii')).hexdigest()
    if digest in seen:duplicates[i]=seen[digest];continue
    seen[digest]=i;colors=np.asarray(g.palette(resource(palettes[i])),dtype='uint8');used=np.unique(a[a!=0])
    banks=[colors[b:b+16] for b in range(0,len(colors)-15,16) if a.max()<16]
    assert banks,(i,'unsupported palette')
    pal=max(banks,key=lambda p:len(np.unique(p[used,:3],axis=0)))
    rgba=pal[a].copy();rgba[:,:,3]=np.where(a,255,0);rgba[a==0,:3]=0
    items.append((i,Image.fromarray(rgba),pal[:,:3].tolist()))
sheets=[];segments=[];canvas=Image.new('RGBA',(512,512));x=y=row=4
def flush():
    global canvas,segments,x,y,row
    if not segments:return
    name=f'late_attack_{len(sheets):03}';canvas.save(OUT/f'{name}_native.png');canvas.resize((2048,2048),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    sheets.append(dict(name=name,native_size=[512,512],reference=f'{name}_reference.png',image=f'{name}_hd.png',segments=segments));canvas=Image.new('RGBA',(512,512));segments=[];x=y=row=4
for i,im,pal in sorted(items,key=lambda p:(-p[1].height,-p[1].width,p[0])):
    w,h=im.size
    if x+w+4>512:x=4;y+=row+8;row=4
    if y+h+4>512:flush()
    assert w<=504 and h<=504
    canvas.paste(im,(x,y));segments.append(dict(resource=i,x=x,y=y,w=w,h=h,palette_rgb=pal));x+=w+8;row=max(row,h)
flush();plan=dict(reviewed_images=len(ids),unique_images=len(items),duplicates=duplicates,sheets=sheets,complete=False)
(OUT/'late_attack_sheets.json').write_text(json.dumps(plan,indent=2));print(json.dumps(dict(images=len(ids),unique=len(items),sheets=len(sheets))))
