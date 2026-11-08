"""Reproduce the game's pre-flip 8x8 -> 2x2 minimap sampling exactly."""

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
ROOT=g.ROOT;FOLDER=ROOT/'graphics/map_tiles'

def main():
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom);cache={}
    def raw(i):
        if i not in cache:cache[i]=g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
        return cache[i]
    path=FOLDER/'catalog.json';catalog=json.loads(path.read_text());report=[]
    for row in catalog['maps']:
        pixels=g.pixels(raw(row['img']));palette=np.array(g.palette(raw(row['pal'])),'uint8')[:,:3];cells=np.frombuffer(raw(row['cel'])[8:],'<u2').reshape(-1,6);m=raw(row['id']);w,h=struct.unpack_from('<HH',m,4);w//=2;h//=2;mi=np.frombuffer(m[8:],'<u2').reshape(h,w);tiny=[]
        for cell in cells:
            block=np.zeros((4,4,3),'uint8')
            for t,e in enumerate(cell[:4]):
                e=int(e);tid=e&1023;full=pixels[tid//32*8:tid//32*8+8,tid%32*8:tid%32*8+8]
                # The game takes rows 0,3 and columns 0,4 BEFORE applying
                # cell H/V flips. Sampling the assembled world loses this.
                idx=full[np.array([0,3])][:,np.array([0,4])];co=palette[(e>>12)*16:(e>>12)*16+16][idx]
                if e&1024:co=co[:,::-1]
                if e&2048:co=co[::-1]
                block[t//2*2:t//2*2+2,t%2*2:t%2*2+2]=co
            tiny.append(block)
        tiny=np.stack(tiny);canvas=tiny[mi].transpose(0,2,1,3,4).reshape(h*4,w*4,3)[8:-8,8:-8];name=f"overview_{row['id']}_native.png";Image.fromarray(canvas).save(FOLDER/name)
        row.update(overview_native=name,overview_size=[canvas.shape[1],canvas.shape[0]],overview_crop=[32,32,w*16-32,h*16-32]);report.append(dict(map=row['id'],width=canvas.shape[1],height=canvas.shape[0]))
    temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(catalog,indent=2));temp.replace(path);library=dict(maps=[r for r in catalog['maps'] if r.get('image')]);path=FOLDER/'library.json';temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(library,indent=2));temp.replace(path);print('Prepared',len(report),'overview references')

if __name__=='__main__':main()
