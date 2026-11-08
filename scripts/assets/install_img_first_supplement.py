"""Append the independently audited IMG-first sources without renumbering parts."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sys,zlib,base64,hashlib
import numpy as np
from PIL import Image
from hd_core import ROOT
sys.path.insert(0,str(ROOT));import scripts.assets.srw_graphics as g

def main():
    folder=ROOT/'graphics/img_first';sheets=json.loads((folder/'sheets.json').read_text())['sheets'];generated=json.loads((folder/'generated_sources.json').read_text())
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    known={b.get('index_hash') for b in bindings if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')};rgb_known={b['hash'] for b in bindings if b.get('rgb_enabled',True) and not b.get('disabled')};blocked=set(meta.get('indexed_collision_keys',[]))
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);records=[]
    for sheet in sheets:
        name=sheet['name'];target=folder/(name+'_hd.png')
        if not target.exists():raise FileNotFoundError(f'Generate and install {target.name} from {name}_reference.png first.')
        meta['atlases'][name]=dict(image='img_first/'+target.name,reference='img_first/'+name+'_native.png',native_size=sheet['native_size'],lazy=True)
        for segment in sheet['segments']:
            i=segment['resource'];idx=g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]));palette=np.asarray(segment['palette_rgb'],dtype='uint32');q=np.rint(palette*31/255).astype('uint16');colors=q[:,0]|q[:,1]<<5|q[:,2]<<10
            for part in segment['unregistered_parts']:
                key=part['index_hash'];x,y,w,h=(part[k] for k in ('x','y','w','h'));a=np.ascontiguousarray(idx[y:y+h,x:x+w]);encoded=np.where(a,colors[a]|0x8000,0).astype('<u2');rgb=zlib.crc32(encoded.tobytes())^(w<<16)^h
                if key in known or key in blocked and rgb in rgb_known:continue
                b=dict(hash=rgb,rgb_enabled=rgb not in rgb_known,index_hash=key,indexed_safe=key not in blocked,dynamic_palette=True,atlas_id=name,resource=i,source_x=x,source_y=y,x=x,y=y+segment['atlas_y'],w=w,h=h,original_palette_rgb=segment['palette_rgb'],index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode(),auto_full_attack=True,img_first_supplement=True,preserve_canonical_paint=True)
                bindings.append(b);known.add(key);rgb_known.add(rgb);records.append(dict(binding=len(bindings),resource=i,index_hash=key,indexed_safe=b['indexed_safe']))
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    path.write_text(json.dumps(meta,indent=2));(folder/'installed.json').write_text(json.dumps(dict(approved_prefix_preserved=True,added=records,all_campaign_replayed=False),indent=2));print('added',len(records))

if __name__=='__main__':main()
