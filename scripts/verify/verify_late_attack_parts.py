"""Validate registered crops against original IMG texels and inspected atlas UVs."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
from functools import lru_cache
import sys,json,zlib
import numpy as np
from PIL import Image
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=128)
def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
@lru_cache(maxsize=4)
def native(path):return np.asarray(Image.open(path).convert('RGBA'))
meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());checked=0;resources=set()
for b in meta['bindings']:
    if not b.get('auto_late_attack'):continue
    s=meta['atlases'][b['atlas_id']];w,h=b['w'],b['h'];x,y=b['source_x'],b['source_y'];a=pixels(b['resource'])[y:y+h,x:x+w]
    key=zlib.crc32(np.where(a,a.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
    assert key==b['index_hash']
    reference=native(ROOT/'graphics'/s['reference'])[b['y']:b['y']+h,b['x']:b['x']+w];assert reference.shape==(h,w,4)
    assert np.array_equal(reference[:,:,3]>0,a>0)
    if b['indexed_safe']:
        used=np.unique(a[a!=0]);pal=np.asarray(b['original_palette_rgb']);assert len(np.unique(pal[used],axis=0))==len(used)
    checked+=1;resources.add(b['resource'])
assert checked>0
result=dict(native_crop_checks=checked,source_images_with_new_bindings=len(resources),palette_and_alpha_checks=True,in_game_all_attacks_verified=False,all_attacks_complete=False)
(OUT/'late_attack_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
