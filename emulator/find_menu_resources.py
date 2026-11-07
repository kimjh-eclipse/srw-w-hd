import json
import numpy as np
import srw_graphics as g
from hd_core import ROOT

def main():
    out=ROOT/'test_current/formation';targets={}
    for index in (25,32,35,36,37,39,40,45):
        a=np.load(out/f'part_{index}.npz')['indices'];blocks=[]
        for y in range(0,a.shape[0],8):
            for x in range(0,a.shape[1],8):
                tile=a[y:y+8,x:x+8];blocks.append((len(np.unique(tile)),int(np.count_nonzero(tile)),tile))
        tile=max(blocks,key=lambda p:p[:2])[2].reshape(-1);needle=(tile[::2]|tile[1::2]<<4).astype('uint8').tobytes();targets[index]=needle
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom);found={};records=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records']
    for r in records:
        if r['kind']!='IMG' or r['bpp']!=4:continue
        i=r['id'];data=g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
        for index,needle in targets.items():
            at=data.find(needle,8)
            if at>=0:found.setdefault(index,[]).append(dict(resource=i,at=at,w=r['w'],h=r['h']))
        if i%100==0:(out/'resource_search_progress.json').write_text(json.dumps(dict(resource=i,found=found)))
    (out/'resource_matches.json').write_text(json.dumps(found,indent=2));print(json.dumps(found))

if __name__=='__main__':main()
