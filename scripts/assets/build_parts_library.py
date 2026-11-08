"""Index original part textures by decoded pixel content, not pose or address."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,zlib
import numpy as np

ROOT=PROJECT_ROOT
raw=np.frombuffer((ROOT/'test_current/robot/vram_65340.bin').read_bytes()[:16384],dtype='uint8')
idx=np.stack([raw&15,raw>>4],-1).reshape(16,32,8,8).transpose(0,2,1,3).reshape(128,256)
pal=np.frombuffer((ROOT/'test_current/robot/pal_65340.bin').read_bytes(),'<u2')[:16]
pixels=np.where(idx!=0,pal[idx]|0x8000,0).astype('<u2')
sizes=[(8,8),(16,16),(32,32),(64,64),(16,8),(32,8),(32,16),(64,32),(8,16),(8,32),(16,32),(32,64)]
bindings=[];seen={}
for w,h in sizes:
    for y in range(0,129-h,8):
        for x in range(0,257-w,8):
            data=pixels[y:y+h,x:x+w].copy();nonzero=data[data!=0]
            if len(nonzero)<3 or len(np.unique(nonzero))<3:continue
            blob=data.tobytes();key=zlib.crc32(blob)^(w<<16)^h
            if key in seen:
                assert seen[key]==blob,'texture CRC collision'
                continue
            seen[key]=blob;bindings.append(dict(hash=key,x=x,y=y,w=w,h=h))
path=ROOT/'graphics/kazuma_parts_library.json'
meta=json.loads(path.read_text()) if path.exists() else dict(native_size=[256,128],atlas='kazuma_parts_atlas_hd.png')
old=meta.get('bindings',[])
if old:
    assert [b['hash'] for b in old[:len(bindings)]]==[b['hash'] for b in bindings],'base binding order changed'
    bindings.extend(b for b in old[len(bindings):] if b['hash'] not in seen)
meta['bindings']=bindings;path.write_text(json.dumps(meta,indent=2))
print(len(bindings),'content-addressed part textures')
