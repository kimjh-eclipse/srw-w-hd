"""Pack newly found basic-unit fragments without changing old UV sheets."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import sys,json,zlib,functools
import numpy as np
from PIL import Image
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts';OUT.mkdir(exist_ok=True)
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@functools.lru_cache(maxsize=128)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
inventory=json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text())
parts=[p for p in inventory['parts'] if p['image']<3480]
sheets=[];items=[];x=y=rowheight=2;canvas=Image.new('RGBA',(256,256))
def flush():
    global canvas,items,x,y,rowheight
    if not items:return
    name=f'basic_extra_{len(sheets):03}'
    canvas.save(OUT/f'{name}_native.png');canvas.resize((2048,2048),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    sheets.append(dict(name=name,native_size=[256,256],reference=f'{name}_reference.png',image=f'{name}_hd.png',parts=items))
    canvas=Image.new('RGBA',(256,256));items=[];x=y=rowheight=2
for part in sorted(parts,key=lambda p:(-p['h'],-p['w'],p['image'],p['index_hash'])):
    w,h=part['w'],part['h']
    if x+w+2>256:x=2;y+=rowheight+4;rowheight=2
    if y+h+2>256:flush()
    indexed=g.pixels(resource(part['image']))[part['y']:part['y']+h,part['x']:part['x']+w]
    palette=np.array(g.palette(resource(part['palette'])),dtype='uint8');bank=part['bank']
    if bank*16+16>len(palette):bank=0
    palette=palette[bank*16:bank*16+16]
    assert len(palette)==16,(part['image'],'no complete palette')
    rgba=palette[indexed].copy();rgba[:,:,3]=np.where(indexed,255,0);rgba[indexed==0,:3]=0
    canvas.paste(Image.fromarray(rgba),(x,y))
    colors=np.frombuffer(resource(part['palette'])[8+bank*32:8+(bank+1)*32],dtype='<u2').astype('uint32')
    encoded=np.where(indexed,colors[indexed]|0x8000,0).astype('<u2')
    items.append(dict(**part,atlas_x=x,atlas_y=y,hash=zlib.crc32(encoded.tobytes())^(w<<16)^h,palette_rgb=palette[:,:3].tolist()))
    x+=w+4;rowheight=max(rowheight,h)
flush();(OUT/'basic_extra_sheets.json').write_text(json.dumps(dict(parts=len(parts),sheets=sheets),indent=2));print(len(parts),len(sheets))
