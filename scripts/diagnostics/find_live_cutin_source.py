"""Search every archive entry, including non-IMG wrappers, for a live BG block."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json,time
from pathlib import Path
from collections import Counter
import numpy as np
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g

def main():
    filename=sys.argv[1] if len(sys.argv)>1 else 'bg_300000_2.npz'
    archive=np.load(g.ROOT/'test_current/attract'/filename);tiles=archive['tiles'].tobytes();base=int.from_bytes(archive['map'].tobytes()[:2],'little')&1023
    needles=[tiles[base*32+1024:base*32+3072],tiles[base*32+4096:base*32+6144]]
    rom=(g.ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);found=[];headers=Counter();start=time.perf_counter()
    for i in range(len(offsets)-1):
        packed=rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]
        try:raw=g.decompress(packed)
        except (ValueError,IndexError):continue
        headers[raw[:4].hex()]+=1
        for n,needle in enumerate(needles):
            at=raw.find(needle)
            if at>=0:found.append(dict(resource=i,needle=n,offset=at,header=raw[:4].hex(),size=len(raw)));print(found[-1],flush=True)
        if i%4000==0:(g.ROOT/'test_current/parts/live_cutin_search_progress.json').write_text(json.dumps(dict(resource=i,seconds=time.perf_counter()-start)))
    (g.ROOT/'test_current/parts/live_cutin_source.json').write_text(json.dumps(dict(found=found,headers=headers.most_common(30)),indent=2));print('finished',found)

if __name__=='__main__':main()
