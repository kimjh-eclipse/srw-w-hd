"""Prepare partial-palette mechanical textures with explicit inherited banks.

Eight-color PLT records contain a prefix, not a complete 16-color OBJ bank.
The preceding full bank is retained for the unmodified suffix. Runtime indexed
bindings still capture the actual palette; this source inheritance is recorded
as an inference until every affected battle has been observed.
"""
import json,sys,hashlib
from pathlib import Path
from functools import lru_cache
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts';TARGET=OUT/'shared_attack_sheets.json'
if TARGET.exists():print('Frozen shared-palette plan');raise SystemExit
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=256)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
pending=json.loads((OUT/'full_attack_blockers.json').read_text())['unresolved_palettes'];items=[]
for row in pending:
    i=row['image'];partial=g.palette(resource(row['palette']));previous=row['palette']-1
    while previous>=0:
        data=resource(previous)
        if data[:4]==b'PLT\0' and len(g.palette(data))>=16:break
        previous-=1
    assert previous>=0,row
    palette=np.asarray(g.palette(resource(previous))[:16],dtype='uint8');palette[:len(partial)]=partial
    a=g.pixels(resource(i));rgba=palette[a].copy();rgba[:,:,3]=np.where(a,255,0);rgba[a==0,:3]=0
    items.append((i,Image.fromarray(rgba),palette[:,:3].tolist(),row['palette'],previous))
sheets=[];segments=[];canvas=Image.new('RGBA',(544,544));x=y=row_height=6
def flush():
    global canvas,segments,x,y,row_height
    if not segments:return
    name=f'shared_attack_{len(sheets):03}';canvas.save(OUT/f'{name}_native.png');canvas.resize((2176,2176),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    sheets.append(dict(name=name,native_size=[544,544],reference=f'{name}_reference.png',image=f'{name}_hd.png',segments=segments));canvas=Image.new('RGBA',(544,544));segments=[];x=y=row_height=6
for i,im,pal,partial,previous in sorted(items,key=lambda p:(-p[1].height,-p[1].width,p[0])):
    w,h=im.size
    if x+w+6>544:x=6;y+=row_height+6;row_height=6
    if y+h+6>544:flush()
    canvas.paste(im,(x,y));segments.append(dict(resource=i,x=x,y=y,w=w,h=h,palette_rgb=pal,partial_palette=partial,inherited_palette=previous,palette_association='inferred prefix overlay; actual runtime palette required'));x+=w+6;row_height=max(row_height,h)
flush();TARGET.write_text(json.dumps(dict(sheets=sheets,source_images=len(items),runtime_palette_verified=False),indent=2));print(len(items),len(sheets))
