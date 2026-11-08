"""Find exact indexed subtextures in already approved HD source atlases.

Only exact native pixel matches are reused. This does not manufacture new art
or treat unmatched animation frames as complete.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import sys,json,zlib,time
import numpy as np
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts';path=ROOT/'graphics/kazuma_parts_library.json'
meta=json.loads(path.read_text());bindings=meta['bindings'];plan=json.loads((ROOT/'graphics/all_units/batches.json').read_text());catalog=json.loads((ROOT/'graphics/all_units/catalog.json').read_text())
inventory=json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text())
for b in bindings:
    approved=inventory['known_index_bindings'].get(str(b.get('index_hash')),0)
    if b.get('auto_animation_reuse') and 0<approved<=4459:
        base=bindings[approved-1];b.update(source_binding=approved,x=base['x'],y=base['y'],original_palette_rgb=meta['source_palette_rgb']);b.pop('atlas_id',None)
active={b['index_hash'] for b in bindings if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}
needed={p['index_hash'] for p in inventory['parts']}|set(map(int,inventory['known_index_bindings']))
needed-=active
needed-=set(meta.get('indexed_collision_keys',[]))
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
sources={s['resource']:("all_"+b['name'],s['batch_y']) for b in plan['batches'] if b.get('required') for s in b['segments']}
sizes=[(8,8),(16,16),(32,32),(64,64),(16,8),(32,8),(32,16),(64,32),(8,16),(8,32),(16,32),(32,64)]
added=0;start=time.time();by_source={}
for package in catalog['packages']:
    source=package['resource']
    if source not in sources or source==7406:continue
    atlas,dy=sources[source];idx=g.pixels(resource(source));height,width=idx.shape
    palette=np.asarray(package['palette_rgb']);encoded=np.where(idx,idx.astype('uint16')|0x8000,0).astype('<u2')
    for w,h in sizes:
        for y in range(0,height-h+1,8):
            for x in range(0,width-w+1,8):
                part=encoded[y:y+h,x:x+w];key=zlib.crc32(part.tobytes())^(w<<16)^h
                if key not in needed:continue
                used=np.unique(idx[y:y+h,x:x+w]);used=used[used!=0]
                if np.count_nonzero(part)<16 or len(used)<3 or len(np.unique(palette[used],axis=0))!=len(used):continue
                spec=dict(hash=0,rgb_enabled=False,index_hash=key,x=x,y=y+dy,w=w,h=h,atlas_id=atlas,dynamic_palette=True,indexed_safe=True,original_palette_rgb=package['palette_rgb'],auto_animation_reuse=True,art_resource=source)
                approved=inventory['known_index_bindings'].get(str(key),0)
                if 0<approved<=4459:
                    base=bindings[approved-1];spec.update(source_binding=approved,x=base['x'],y=base['y'],original_palette_rgb=meta['source_palette_rgb']);spec.pop('atlas_id',None)
                bindings.append(spec)
                needed.remove(key);active.add(key);added+=1;by_source[source]=by_source.get(source,0)+1
    if added and added%100==0:(OUT/'reuse_progress.json').write_text(json.dumps(dict(added=added,source=source,seconds=round(time.time()-start,1))))
assert len(bindings)<100000,'Core binding capacity exceeded'
path.write_text(json.dumps(meta,indent=2));result=dict(exact_reused_parts=sum(bool(b.get('auto_animation_reuse')) and b.get('index_hash') not in meta.get('indexed_collision_keys',[]) for b in bindings),added_this_run=added,total_bindings=len(bindings),by_source=by_source,seconds=round(time.time()-start,1),unmatched_inventory_patterns=len(needed),complete=False)
(OUT/'reuse_report.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='by_source'}))
