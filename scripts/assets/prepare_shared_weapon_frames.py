"""Extract the observed shared rocket-punch IMG animation for precise painting."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    folder=ROOT/'graphics/shared_weapon_frames';folder.mkdir(exist_ok=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def read(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    # The archive's neighboring PLT is a recoloring template (blue fists),
    # not the live weapon palette. Use a captured native punch material.
    observed=json.loads((folder/'observed_palette.json').read_text())
    values=np.asarray(observed['palette'],dtype='uint32')
    live_rgb=np.stack([(values&31)*255//31,((values>>5)&31)*255//31,((values>>10)&31)*255//31],-1).astype('uint8')
    rgb=np.asarray(g.palette(read(20712)),dtype='uint8')[:16,:3].copy();rgb[9:]=live_rgb[9:];sheets=[]
    resources=list(range(20713,20750))
    for page in range(4):
        canvas=Image.new('RGBA',(160,400));items=[]
        for slot,resource in enumerate(resources[page*10:(page+1)*10]):
            a=g.pixels(read(resource));h,w=a.shape;assert w<=80 and h<=80
            rgba=np.dstack([rgb[a],(a!=0).astype('uint8')*255]);rgba[a==0]=0
            x,y=(slot%2)*80,(slot//2)*80;canvas.paste(Image.fromarray(rgba),(x,y))
            items.append(dict(resource=resource,slot=slot,x=x,y=y,w=w,h=h,palette_rgb=rgb.tolist()))
        name=f'rocket_punch_{page:02}';canvas.save(folder/f'{name}_native.png');canvas.resize((640,1600),Image.Resampling.NEAREST).save(folder/f'{name}_reference.png')
        sheets.append(dict(name=name,output=f'{name}_generated.png',native_size=[160,400],items=items))
    (folder/'plan.json').write_text(json.dumps(dict(scope='Observed Mazinger-family shared punch animation IMG 20713..20749',sheets=sheets),indent=2))

if __name__=='__main__':main()
