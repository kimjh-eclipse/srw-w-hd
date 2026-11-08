"""Find every IMG/PLT/PAT order missed by the original PLT-first extractor."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,zlib,hashlib,sys
from pathlib import Path
import numpy as np
from hd_core import ROOT
sys.path.insert(0,str(ROOT))
import scripts.assets.srw_graphics as g

def main():
    records=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];byid={r['id']:r for r in records}
    packages=json.loads((ROOT/'graphics/all_units/catalog.json').read_text())['packages'];extracted={p['resource'] for p in packages}
    audit=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text());patterns={p['pattern']:p for p in audit['patterns']}
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());resources={b.get('resource') for b in library['bindings'] if not b.get('disabled')}
    known={b.get('index_hash') for b in library['bindings'] if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}
    blocked=set(library.get('indexed_collision_keys',[]));known-=blocked
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);report=[]
    for r in records:
        i=r['id']
        if r['kind']!='IMG' or byid.get(i+1,{}).get('kind')!='PLT' or byid.get(i+2,{}).get('kind')!='PAT':continue
        pattern=patterns.get(i+2,{})
        pixels=g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]));keys=set();missing=[]
        for part in pattern.get('parts',[]):
            x=part['tile']%32*8;y=part['tile']//32*8;w=part['w'];h=part['h'];a=pixels[y:y+h,x:x+w]
            if a.shape!=(h,w) or np.count_nonzero(a)<24 or len(np.unique(a[a!=0]))<3:continue
            data=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');key=zlib.crc32(data.tobytes())^(w<<16)^h
            if key in keys:continue
            keys.add(key)
            if key not in known:missing.append(dict(index_hash=key,x=x,y=y,w=w,h=h,collision=key in blocked))
        report.append(dict(resource=i,palette=i+1,pattern=i+2,width=r['w'],height=r['h'],poses=pattern.get('poses'),parsed_parts=pattern.get('records'),eligible_unique_parts=len(keys),unregistered_parts=missing,present_in_original_extractor=i in extracted,has_registered_source=i in resources))
    result=dict(packages=report,total=len(report),missed_by_original_extractor=sum(not p['present_in_original_extractor'] for p in report),unregistered_unique_parts=sum(len(p['unregistered_parts']) for p in report),resources_using_shared_bindings=[p['resource'] for p in report if not p['has_registered_source']],scope='Archive structure and registered source coverage. A source registration is not proof that every weapon has been replayed.')
    (ROOT/'test_current/rom_catalog/img_first_audit.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='packages'}))

if __name__=='__main__':main()
