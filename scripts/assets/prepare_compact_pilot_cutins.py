"""Assemble compact combined-pilot IMG/SCR pictures before painting them."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    folder=ROOT/'graphics/compact_pilot_cutins';folder.mkdir(exist_ok=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def read(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    # These PLTs replace palette banks at successive animation phases; they
    # are not one concatenated palette. The initial 112-color PLT alone
    # covers the three opening faces. Exact live BG palette banks confirm
    # 23467 at frame 600 and 23468/23470 at frame 720.
    palette_ids={23473:23465,23474:23465,23475:23465,23476:23466,
        23477:23467,23478:23468,23479:23469,23480:23470,
        23481:23471,23482:23471,23483:23472}
    rows=[];cards=[]
    for image in range(23473,23484):
        palette_id=palette_ids[image];colors=np.asarray(g.palette(read(palette_id)),dtype='uint8')
        map_id=image+11;data=read(map_id);assert data[:4]==b'SCR\0'
        w,h=int(data[5])*8,int(data[6])*8;entries=np.frombuffer(data[8:],dtype='<u2').reshape(h//8,w//8)
        a=g.pixels(read(image));canvas=np.zeros((h,w,4),dtype='uint8')
        for y in range(h//8):
            for x in range(w//8):
                entry=int(entries[y,x]);tile=entry&1023;sx=tile%32*8;sy=tile//32*8;native=a[sy:sy+8,sx:sx+8]
                if native.shape!=(8,8):continue
                palette=colors[(entry>>12)*16:((entry>>12)+1)*16];assert len(palette)==16
                rgba=palette[native].copy();rgba[native==0]=0
                if entry&1024:rgba=rgba[:,::-1]
                if entry&2048:rgba=rgba[::-1]
                canvas[y*8:y*8+8,x*8:x*8+8]=rgba
        im=Image.fromarray(canvas);im.save(folder/f'cutin_{image}_native.png')
        im.resize((768,384),Image.Resampling.NEAREST).save(folder/f'cutin_{image}_reference.png')
        rows.append(dict(resource=image,map=map_id,palettes=[palette_id],native_size=[w,h],reference=f'cutin_{image}_reference.png',output=f'cutin_{image}_generated.png'))
        thumb=im.resize((384,192),Image.Resampling.NEAREST);card=Image.new('RGB',(384,216),'#26333f');card.paste(thumb,(0,24),thumb);ImageDraw.Draw(card).text((4,4),str(image),fill='white');cards.append(card)
    contact=Image.new('RGB',(1152,216*4),'#26333f')
    for i,card in enumerate(cards):contact.paste(card,(i%3*384,i//3*216))
    out=ROOT/'test_current/parts/compact_pilot_cutins';out.mkdir(exist_ok=True);contact.save(out/'contact.png')
    (folder/'plan.json').write_text(json.dumps(dict(scope=__doc__,items=rows),indent=2));print('Assembled',len(rows),'compact cut-in pictures')

if __name__=='__main__':main()
