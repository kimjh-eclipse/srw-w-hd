import json,sys
import numpy as np
from PIL import Image,ImageDraw
from hd_core import ROOT
sys.path.insert(0,str(ROOT))
from srw_graphics import archive,decompress,pixels,palette,BASE

def main():
    folder=ROOT/'graphics/map_icons';rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=archive(rom)
    targets={}
    for name in ('7eb4729b','5c659077'):
        a=np.load(folder/(name+'_native.npz'))['indices'];t=a[:8,:8];targets[name]=np.packbits(np.empty(0)) if False else (t[:,::2]|(t[:,1::2]<<4)).tobytes()
    catalog=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];matches=[]
    for r in catalog:
        if r['kind']!='IMG' or r['bpp']!=4:continue
        i=r['id'];raw=decompress(rom[BASE+offsets[i]:BASE+offsets[i+1]])
        for name,needle in targets.items():
            at=raw.find(needle,8)
            if at>=0:matches.append(dict(resource=i,target=name,offset=at,w=r['w'],h=r['h']))
    (folder/'resource_matches.json').write_text(json.dumps(matches,indent=2));print(json.dumps(matches))
    for i in sorted({r['resource'] for r in matches}):
        raw=decompress(rom[BASE+offsets[i]:BASE+offsets[i+1]]);a=pixels(raw);Image.fromarray((a*17).astype('uint8')).save(folder/f'resource_{i}_indices.png')

if __name__=='__main__':main()
