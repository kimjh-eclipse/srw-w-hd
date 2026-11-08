"""Measure exact tile reuse before inventing or painting replacement art."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
from functools import lru_cache
import sys,json,hashlib
import numpy as np
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=128)
def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
def tiles(a):
    h,w=a.shape
    for y in range(0,h-7,8):
        for x in range(0,w-7,8):yield x,y,a[y:y+8,x:x+8].tobytes()
plan=json.loads((ROOT/'graphics/all_units/batches.json').read_text())
known={}
for sheet in plan['batches']:
    if not sheet.get('required'):continue
    for s in sheet['segments']:
        if s['resource']==7406:continue
        for x,y,key in tiles(pixels(s['resource'])):
            if any(key):known.setdefault(key,dict(atlas_id='all_'+sheet['name'],x=x,y=y+s['batch_y'],resource=s['resource']))
extra=json.loads((OUT/'basic_extra_sheets.json').read_text())
for sheet in extra['sheets']:
    if not (OUT/sheet['image']).exists():continue
    for p in sheet['parts']:
        a=pixels(p['image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        for x,y,key in tiles(a):
            if any(key):known.setdefault(key,dict(atlas_id=sheet['name'],x=x+p['atlas_x'],y=y+p['atlas_y'],resource=p['image']))
inventory=json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text())
meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
active={b.get('index_hash') for b in meta['bindings'] if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}
complete=[];partial=none=0;new_tiles=set()
for p in inventory['parts']:
    if p['index_hash'] in active or not 6995<=p['image']<19700:continue
    a=pixels(p['image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
    keys=[key for _,_,key in tiles(a) if any(key)];missing=[k for k in keys if k not in known]
    new_tiles.update(missing)
    if not missing:complete.append(p['index_hash'])
    elif len(missing)<len(keys):partial+=1
    else:none+=1
report=dict(known_unique_tiles=len(known),fully_reusable_candidate_parts=len(complete),partially_reusable_candidate_parts=partial,no_tile_reuse=none,missing_unique_tiles=len(new_tiles),complete_index_hashes=complete,scope_note='Conservative IMG/PAT candidates; includes attached effects and unresolved group pairings. Not completion proof.')
(OUT/'tile_reuse_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='complete_index_hashes'}))
