"""Use the actual Sandrock combat palette for its enlarged attack-parts atlas."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sys,zlib,base64
import numpy as np
from PIL import Image
from hd_core import ROOT
sys.path.insert(0,str(ROOT));import scripts.assets.srw_graphics as g

def main():
    folder=ROOT/'graphics/wing_parts'
    if not (folder/'sandrock_closeup_hd.png').exists():raise FileNotFoundError('Install sandrock_closeup_hd.png from sandrock_closeup_reference.png first.')
    native=np.asarray(Image.open(folder/'sandrock_closeup_native.png'))
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);idx=g.pixels(g.decompress(rom[g.BASE+offsets[7278]:g.BASE+offsets[7279]]))
    colors=np.asarray(json.loads((ROOT/'test_current/attract/obj_300002.json').read_text())[4]['palette_colors'],dtype='uint16')
    rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('uint8')
    # uint16 multiplication above remains within range (31*255).
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());meta['atlases']['wing_closeup']=dict(image='wing_parts/sandrock_closeup_hd.png',reference='wing_parts/sandrock_closeup_native.png',native_size=[256,128],lazy=True)
    updated=[]
    for i,b in enumerate(meta['bindings'],1):
        if i<=5263 or b.get('resource')!=7278:continue
        x=b.get('source_x',b['x']);y=b.get('source_y',b['y']);w=b['w'];h=b['h'];a=idx[y:y+h,x:x+w]
        if a.shape!=(h,w):continue
        encoded=np.where(a,colors[a]|0x8000,0).astype('<u2');b.update(atlas_id='wing_closeup',x=x,y=y,source_x=x,source_y=y,original_palette_rgb=rgb.tolist(),hash=zlib.crc32(encoded.tobytes())^(w<<16)^h,index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode(),wing_live_palette=True)
        for key in ('source_binding','palette_source_rgb','palette_rgb'):b.pop(key,None)
        updated.append(i)
    path.write_text(json.dumps(meta,indent=2));(folder/'closeup_installed.json').write_text(json.dumps(dict(resource=7278,updated=updated,palette_rgb=rgb.tolist(),native_size=[256,128]),indent=2));print(len(updated))

if __name__=='__main__':main()
