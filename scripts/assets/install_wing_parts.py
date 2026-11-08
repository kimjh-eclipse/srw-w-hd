"""Register omitted IMG-first Wing source rectangles without renumbering assets."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json,hashlib,zlib,base64
from pathlib import Path
import numpy as np
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g

def main():
    path=g.ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    for binding in bindings:
        if binding.get('wing_img_first'):binding['auto_unit']=True
    rom=(g.ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    meta.setdefault('atlases',{})['wing_primary']=dict(image='wing_parts/primary_hd.png',reference='wing_parts/primary_native.png',native_size=[256,64],lazy=True)
    active={b.get('index_hash') for b in bindings if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')};blocked=set(meta.get('indexed_collision_keys',[]));known={b['hash'] for b in bindings if b.get('rgb_enabled',True) and not b.get('disabled')};records=[]
    canonical={b['index_hash']:i for i,b in enumerate(bindings,1) if b.get('wing_img_first')}
    for source,dy in ((1164,0),(1180,32)):
        pixels=g.pixels(resource(source));palette=np.asarray(g.palette(resource(source+1)),dtype='uint8')[:16,:3];native=np.frombuffer(resource(source+1)[8:40],dtype='<u2')
        for w,h in ((8,8),(16,16),(32,32),(64,64),(16,8),(32,8),(32,16),(64,32),(8,16),(8,32),(16,32),(32,64)):
            for y in range(0,pixels.shape[0]-h+1,8):
                for x in range(0,pixels.shape[1]-w+1,8):
                    a=np.ascontiguousarray(pixels[y:y+h,x:x+w]);used=np.unique(a[a!=0])
                    if np.count_nonzero(a)<24 or len(used)<3:continue
                    indexed=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');key=zlib.crc32(indexed.tobytes())^(w<<16)^h
                    if key in canonical or key in blocked:continue
                    encoded=np.where(a,native[a]|0x8000,0).astype('<u2');rgb_key=zlib.crc32(encoded.tobytes())^(w<<16)^h
                    spec=dict(hash=rgb_key,rgb_enabled=rgb_key not in known,index_hash=key,indexed_safe=True,dynamic_palette=True,atlas_id='wing_primary',resource=source,source_x=x,source_y=y,x=x,y=y+dy,w=w,h=h,original_palette_rgb=palette.tolist(),index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),wing_img_first=True,auto_unit=True)
                    bindings.append(spec);active.add(key);canonical[key]=len(bindings);known.add(rgb_key);records.append(dict(binding=len(bindings),resource=source,x=x,y=y,w=w,h=h))
    relinked=[]
    for identifier,binding in enumerate(bindings,1):
        key=binding.get('index_hash');resource_id=binding.get('resource',-1)
        if identifier<=5263 or binding.get('wing_img_first') or key not in canonical or not 6995<=resource_id<=7418:continue
        source=bindings[canonical[key]-1];old_palette=binding['original_palette_rgb']
        binding.update(source_binding=canonical[key],palette_source_rgb=source['original_palette_rgb'],original_palette_rgb=source['original_palette_rgb'],index_pixels=source['index_pixels'],wing_source_relinked=True)
        if old_palette!=source['original_palette_rgb']:binding['palette_rgb']=old_palette
        relinked.append(identifier)
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    assert len(bindings)<200000
    temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(meta,indent=2));temporary.replace(path)
    all_records=[dict(binding=i,resource=b['resource'],x=b['source_x'],y=b['source_y'],w=b['w'],h=b['h']) for i,b in enumerate(bindings,1) if b.get('wing_img_first')]
    (g.ROOT/'graphics/wing_parts/installed.json').write_text(json.dumps(dict(added_this_run=len(records),total=len(all_records),records=all_records,relinked=relinked,approved_prefix_preserved=True,all_attacks_verified=False),indent=2));print(len(records),len(all_records),'relinked',len(relinked))

if __name__=='__main__':main()
