"""Check added identities against native pixels, not just CRC coincidences."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
from functools import lru_cache
import sys,json,zlib
import numpy as np
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=128)
def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());bindings=meta['bindings']
inventory=json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text())
targets={p['index_hash']:p for p in inventory['parts']}
raw=np.frombuffer((ROOT/'test_current/robot/vram_65340.bin').read_bytes()[:16384],dtype='uint8')
hero=np.stack([raw&15,raw>>4],-1).reshape(16,32,8,8).transpose(0,2,1,3).reshape(128,256)
def key(a):
    h,w=a.shape;return zlib.crc32(np.where(a,a.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h
known={}
for i,b in enumerate(bindings[:4459],1):
    a=hero[b['y']:b['y']+b['h'],b['x']:b['x']+b['w']];known.setdefault(key(a),a)
plan=json.loads((ROOT/'graphics/all_units/batches.json').read_text())
segments={("all_"+batch['name'],s['resource']):s['batch_y'] for batch in plan['batches'] for s in batch['segments']}
exact=approved=0;errors=[];guarded=[]
for i,b in enumerate(bindings,1):
    if not b.get('auto_animation_reuse'):continue
    k=b['index_hash'];t=targets.get(k)
    if t is not None:expected=pixels(t['image'])[t['y']:t['y']+t['h'],t['x']:t['x']+t['w']]
    else:expected=known[k]
    if b.get('source_binding'):
        s=bindings[b['source_binding']-1];a=hero[s['y']:s['y']+s['h'],s['x']:s['x']+s['w']];approved+=1
    else:
        source=b['art_resource'];y=b['y']-segments[(b['atlas_id'],source)];a=pixels(source)[y:y+b['h'],b['x']:b['x']+b['w']]
    if not np.array_equal(expected,a):
        entry=dict(binding=i,index_hash=k,reason='CRC collision or wrong source rectangle')
        (guarded if k in meta.get('indexed_collision_keys',[]) else errors).append(entry)
    exact+=1
extra=json.loads((OUT/'basic_extra_sheets.json').read_text());extra_count=0
for sheet in extra['sheets']:
    for p in sheet['parts']:
        a=pixels(p['image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        assert key(a)==p['index_hash'],p
        assert any(b['hash']==p['hash'] and not b.get('disabled') for b in bindings),p
        extra_count+=1
disabled=sum(b.get('disabled',False) and b.get('resource')==7406 for b in bindings)
assert disabled>0 and all(b.get('disabled') for b in bindings if b.get('auto_unit') and b.get('resource')==7406)
result=dict(reuse_candidates_checked=exact,exact_reuse_active=exact-len(guarded),approved_face_sources_reused=approved,new_basic_candidates_checked=extra_count,disabled_pilot_eye_bindings=disabled,blocked_index_collisions=guarded,identity_errors=errors,all_attacks_complete=False)
(OUT/'verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not errors
