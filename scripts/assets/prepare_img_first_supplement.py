"""Stage omitted source sheets separately, keeping approved packing untouched."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sys
import numpy as np
from PIL import Image,ImageDraw
from hd_core import ROOT
sys.path.insert(0,str(ROOT));import scripts.assets.srw_graphics as g

def main():
    packages=json.loads((ROOT/'test_current/rom_catalog/img_first_audit.json').read_text())['packages']
    if not any(p['unregistered_parts'] for p in packages) and (ROOT/'graphics/img_first/sheets.json').exists():
        print('All audited parts registered; preserving the installed atlas plan.');return
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    out=ROOT/'graphics/img_first';out.mkdir(exist_ok=True);sheets=[];segments=[];canvas=Image.new('RGBA',(256,256));cursor=0
    review=Image.new('RGB',(1280,((len(packages)+4)//5)*190),(35,35,40));draw=ImageDraw.Draw(review)
    def flush():
        nonlocal canvas,cursor,segments
        if not segments:return
        name=f'omitted_{len(sheets):02}';native=canvas.crop((0,0,256,cursor));native.save(out/(name+'_native.png'));native.resize((960,round(cursor*3.75)),Image.Resampling.NEAREST).save(out/(name+'_reference.png'))
        sheets.append(dict(name=name,native_size=list(native.size),segments=segments));canvas=Image.new('RGBA',(256,256));cursor=0;segments=[]
    for n,p in enumerate(packages):
        i=p['resource'];idx=g.pixels(resource(i));pal=np.asarray(g.palette(resource(i+1)),dtype='uint8');rgba=pal[idx].copy();rgba[:,:,3]=(idx!=0)*255;rgba[idx==0,:3]=0;im=Image.fromarray(rgba)
        x=n%5*256;y=n//5*190;review.paste(im,(x,y+20),im);draw.text((x,y),str(i),fill='white')
        if not p['unregistered_parts']:continue
        if cursor+im.height>256:flush()
        canvas.alpha_composite(im,(0,cursor));segments.append(dict(p,atlas_x=0,atlas_y=cursor,palette_rgb=pal[:16,:3].tolist()));cursor+=im.height
    flush();(out/'sheets.json').write_text(json.dumps(dict(sheets=sheets),indent=2));review.save(ROOT/'test_current/parts/img_first_review.png');print([(s['name'],s['native_size']) for s in sheets])

if __name__=='__main__':main()
