"""Review early full-screen pilot images with their adjacent palettes."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g

def main():
    rom=(g.ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    rows=json.loads((g.ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];kinds={r['id']:r['kind'] for r in rows};last=None;images=[]
    start,end=(map(int,sys.argv[1:3]) if len(sys.argv)>2 else (4395,6098))
    out=g.ROOT/'test_current/parts'
    for row in rows:
        i=row['id']
        if row['kind']=='PLT':last=i
        if row['kind']!='IMG' or not start<=i<end or row.get('w',0)<64 or row.get('h',0)<32:continue
        palette_id=i+1 if kinds.get(i+1)=='PLT' else last
        indices=g.pixels(resource(i));palette=np.asarray(g.palette(resource(palette_id)),dtype='uint8')
        if indices.max()>=len(palette):continue
        rgba=palette[indices].copy();rgba[:,:,3]=(indices!=0)*255;im=Image.fromarray(rgba);im.thumbnail((150,150));images.append((i,im))
    sheet=Image.new('RGB',(160*10,175*((len(images)+9)//10)),(30,35,43));draw=ImageDraw.Draw(sheet)
    for j,(i,im) in enumerate(images):
        sheet.paste(im,(j%10*160,j//10*175+20),im);draw.text((j%10*160,j//10*175),str(i),fill='white')
    sheet.save(out/'wing_cutin_sources.png');print(len(images))

if __name__=='__main__':main()
