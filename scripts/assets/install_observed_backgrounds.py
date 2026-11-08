
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,zlib,shutil
import numpy as np
from pathlib import Path
from PIL import Image
ROOT=PROJECT_ROOT;OUT=ROOT/'graphics/backgrounds'
items=[]
for frame,name,layer in [(8910,'city',3),(7040,'field',3),(8910,'tower',2),(13110,'space',3),(14850,'deck',3),(8100,'forest',3)]:
    source=ROOT/f'test_current/attract/bg_{frame}_{layer}.npz';raw=np.load(source);info=raw['info'];maps=raw['map'];count=(int(np.max(maps.view('<u2')&1023))+1)*(64 if info[0]&128 else 32)
    if not (OUT/f'{name}_hd.png').exists():continue
    shutil.copyfile(ROOT/f'test_current/attract/bg_{frame}_{layer}.png',OUT/f'{name}_native.png')
    image=f'{name}_hd.png'
    if name=='tower':
        # Pack the redrawn cutout back into its original 512x256 tilemap UVs.
        canvas=Image.new('RGBA',(512*8,256*8));paint=Image.open(OUT/image).convert('RGBA').resize((136*8,104*8),Image.Resampling.LANCZOS);canvas.paste(paint,(0,0));image='tower_atlas.png';canvas.save(OUT/image)
    tile_size=64 if info[0]&128 else 32;indices=np.unique(maps.view('<u2')&1023)
    referenced=raw['tiles'][:count].reshape(-1,tile_size)[indices].tobytes()
    items.append(dict(id=len(items)+1,name=name,layer=layer,image=f'backgrounds/{image}',native=f'backgrounds/{name}_native.png',tile_bytes=count,tile_size=tile_size,tile_indices=indices.tolist(),signatures=[[zlib.crc32(referenced),zlib.crc32(maps.tobytes())]]))
(OUT/'library.json').write_text(json.dumps(dict(backgrounds=items),indent=2));print('registered',len(items))
