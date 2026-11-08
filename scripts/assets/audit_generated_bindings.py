"""Validate generated identities and keep flat-color UI shapes out of RGB lookup."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,zlib,base64,hashlib,sys
from pathlib import Path
from functools import lru_cache
import numpy as np
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT

def main():
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    @lru_cache(maxsize=256)
    def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
    checked=guarded=0;errors=[];identities={};collisions=set(meta.get('indexed_collision_keys',[]))
    for i,b in enumerate(bindings,1):
        if not (b.get('auto_full_attack') or b.get('auto_shared_attack')):continue
        a=pixels(b['resource'])[b['source_y']:b['source_y']+b['h'],b['source_x']:b['source_x']+b['w']]
        encoded=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');key=zlib.crc32(encoded.tobytes())^(b['w']<<16)^b['h']
        if a.shape!=(b['h'],b['w']) or key!=b['index_hash']:errors.append(i);continue
        if b.get('index_pixels') and not np.array_equal(a,np.frombuffer(zlib.decompress(base64.b64decode(b['index_pixels'])),dtype='uint8').reshape(a.shape)):errors.append(i);continue
        digest=hashlib.sha256(a.tobytes()+str(a.shape).encode()).digest()
        if key in identities and identities[key]!=digest:collisions.add(key)
        identities[key]=digest
        palette=np.asarray(b['original_palette_rgb']);unique=len(np.unique(palette[np.unique(a[a!=0])],axis=0))
        if unique<3 and b.get('rgb_enabled',True):b['rgb_enabled']=False;guarded+=1
        checked+=1
    assert not errors,errors[:20]
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    meta['indexed_collision_keys']=sorted(collisions)
    temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(meta,indent=2));temp.replace(path)
    report=dict(checked=checked,identity_errors=errors,flat_rgb_shapes_guarded=guarded,blocked_index_hashes=len(collisions),prefix_preserved=True)
    (ROOT/'test_current/parts/generated_bindings_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
