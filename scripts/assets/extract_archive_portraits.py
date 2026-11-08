"""Read W's paired 56x48 portrait IMG/PLT archive entries."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=PROJECT_ROOT;sys.path.insert(0,str(ROOT))
import scripts.assets.srw_graphics as g
OUT=ROOT/'graphics/portraits/archive';OUT.mkdir(exist_ok=True)
TEST=ROOT/'test_current/portrait';TEST.mkdir(exist_ok=True)
def main():
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    records=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];byid={r['id']:r for r in records};items=[]
    for record in records:
        if record['kind']!='IMG' or (record['w'],record['h'])!=(56,48):continue
        i=record['id'];p=byid.get(i+1)
        if not p or p['kind']!='PLT' or p['colors']!=16:continue
        idx=g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
        colors=np.array(g.palette(g.decompress(rom[g.BASE+offsets[i+1]:g.BASE+offsets[i+2]])),dtype='uint8')
        rgba=colors[idx].copy();rgba[idx==0]=0;im=Image.fromarray(rgba)
        name=f'portrait_{i:05}';im.save(OUT/f'{name}_native.png')
        im.resize((1008,864),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
        items.append(dict(name=name,img=i,plt=i+1,index_crc32=zlib.crc32(idx.tobytes()),path=f'archive/{name}_native.png'))
    for page in range((len(items)+63)//64):
        s=Image.new('RGB',(896,896),'#283038');d=ImageDraw.Draw(s)
        for n,item in enumerate(items[page*64:page*64+64]):
            im=Image.open(OUT/(item['name']+'_native.png')).resize((112,96),Image.Resampling.NEAREST);x=n%8*112;y=n//8*112
            s.paste(im,(x,y),im);d.text((x+4,y+97),str(item['img']),fill='white')
        s.save(TEST/f'archive_review_{page:02}.png')
    (OUT/'catalog.json').write_text(json.dumps(dict(portraits=items),indent=2));print(len(items))
if __name__=='__main__':main()
