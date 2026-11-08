"""Decode SCR tile maps and palette banks for the requested eye cut-ins."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json,struct
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g

def main():
    rom=(g.ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    out=g.ROOT/'graphics/wing_parts';records=[]
    for name,identifier in (('duo',23282),('quatre',23288)):
        raw=resource(identifier);indices=g.pixels(raw);pal=np.asarray(g.palette(resource(identifier-1)),dtype='uint8');data=resource(identifier+1)
        assert data[:4]==b'SCR\0';width,height=data[5]*8,data[6]*8;entries=np.frombuffer(data[8:],dtype='<u2').reshape(height//8,width//8)
        canvas=np.zeros((192,256,4),dtype='uint8')
        for ty,row in enumerate(entries):
            for tx,entry in enumerate(row):
                tile=int(entry)&1023;x=tile%32*8;y=tile//32*8;a=indices[y:y+8,x:x+8]
                if a.shape!=(8,8):continue
                colors=pal[(int(entry)>>12)*16:((int(entry)>>12)+1)*16]
                if len(colors)<16:continue
                rgba=colors[a].copy();rgba[:,:,3]=(a!=0)*255
                if entry&1024:rgba=rgba[:,::-1]
                if entry&2048:rgba=rgba[::-1]
                canvas[ty*8:ty*8+8,tx*8:tx*8+8]=rgba
        native=Image.fromarray(canvas);native.save(out/(name+'_cutin_native.png'));native.resize((960,720),Image.Resampling.NEAREST).save(out/(name+'_cutin_reference.png'))
        signature=2166136261
        for value in raw[8+1024:8+3072]:signature=((signature^value)*16777619)&0xffffffff
        records.append(dict(name=name,resource=identifier,palette=identifier-1,map=identifier+1,signature=signature,native_size=[256,192],scr_size=[width,height]))
    (out/'cutin_sources.json').write_text(json.dumps(records,indent=2));print(records)

if __name__=='__main__':main()
