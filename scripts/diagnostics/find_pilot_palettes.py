"""Rank large IMG resources by overlap with requested pilots' native colors."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g

def main():
    rom=(g.ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    rows=json.loads((g.ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];kinds={r['id']:r['kind'] for r in rows};palettes={};last=None;candidates=[]
    requested={i:set(map(tuple,np.asarray(g.palette(resource(i+1)))[:,:3])) for i in (56,60)}
    for row in rows:
        i=row['id']
        if row['kind']=='PLT':last=i;palettes[i]=np.asarray(g.palette(resource(i)),dtype='uint8')
        if row['kind']!='IMG' or row.get('w',0)<80 or row.get('h',0)<40:continue
        palette_id=i+1 if kinds.get(i+1)=='PLT' else last
        if palette_id not in palettes:palettes[palette_id]=np.asarray(g.palette(resource(palette_id)),dtype='uint8')
        palette=palettes[palette_id];colors=set(map(tuple,palette[:16,:3]));scores={p:len(colors&ref) for p,ref in requested.items()}
        candidates.append(dict(resource=i,palette=palette_id,score=max(scores.values()),scores=scores))
    result=sorted(candidates,key=lambda r:-r['score'])[:70];out=g.ROOT/'test_current/parts';sheet=Image.new('RGB',(160*10,175*7),(30,35,43));draw=ImageDraw.Draw(sheet)
    for n,r in enumerate(result):
        a=g.pixels(resource(r['resource']));palette=palettes[r['palette']]
        if a.max()>=len(palette):continue
        rgba=palette[a].copy();rgba[:,:,3]=(a!=0)*255;im=Image.fromarray(rgba);im.thumbnail((150,150));sheet.paste(im,(n%10*160,n//10*175+20),im);draw.text((n%10*160,n//10*175),f"{r['resource']} {r['score']}",fill='white')
    sheet.save(out/'pilot_palette_candidates.png');(out/'pilot_palette_candidates.json').write_text(json.dumps(result,indent=2));print(result[:5])

if __name__=='__main__':main()
