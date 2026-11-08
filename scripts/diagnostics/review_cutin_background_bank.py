"""Decode every large late-bank BG family for a complete visual scope review."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
import json,struct
from functools import lru_cache
import numpy as np
from PIL import Image,ImageDraw

def main():
    folder=ROOT/'test_current/parts/cutin_bank';folder.mkdir(exist_ok=True)
    inventory=json.loads((ROOT/'test_current/parts/cutin_bg_inventory.json').read_text())
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    @lru_cache(maxsize=32)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    groups={}
    for row in inventory['groups']:
        previous=groups.get(row[1])
        if previous is None or row[3]*row[4]>previous[3]*previous[4]:groups[row[1]]=row
    rows=[];cards=[]
    for palette,image,mapid,w,h in groups.values():
        try:
            indices=g.pixels(resource(image));colors=np.asarray(g.palette(resource(palette)),dtype='uint8')
            data=resource(mapid);entries=np.frombuffer(data[8:8+(w//8)*(h//8)*2],dtype='<u2').reshape(h//8,w//8)
            canvas=np.zeros((h,w,4),dtype='uint8')
            for ty,row in enumerate(entries):
                for tx,entry in enumerate(row):
                    tile=int(entry)&1023;x=tile%32*8;y=tile//32*8;a=indices[y:y+8,x:x+8]
                    bank=int(entry)>>12;pal=colors[bank*16:(bank+1)*16]
                    if a.shape!=(8,8) or len(pal)<16:continue
                    rgba=pal[a].copy();rgba[a==0]=0
                    if entry&1024:rgba=rgba[:,::-1]
                    if entry&2048:rgba=rgba[::-1]
                    canvas[ty*8:ty*8+8,tx*8:tx*8+8]=rgba
            im=Image.fromarray(canvas);im.save(folder/f'bg_{image}_native.png')
            thumb=im.copy();thumb.thumbnail((128,96));card=Image.new('RGB',(128,112),'#29313c');card.paste(thumb,(0,0),thumb);ImageDraw.Draw(card).text((2,96),str(image),fill='white');cards.append(card)
            rows.append(dict(image=image,palette=palette,map=mapid,size=[w,h],opaque=int(np.count_nonzero(canvas[:,:,3]))))
        except (ValueError,IndexError,AssertionError,struct.error) as error:
            rows.append(dict(image=image,error=str(error)))
    for page in range((len(cards)+63)//64):
        sheet=Image.new('RGB',(1024,896),'#29313c')
        for i,card in enumerate(cards[page*64:page*64+64]):sheet.paste(card,(i%8*128,i//8*112))
        sheet.save(folder/f'contact_{page:02}.png')
    (folder/'inventory.json').write_text(json.dumps(dict(scope='Unclassified decoded BG families; requires visual classification',images=rows),indent=2))
    print('decoded',len(cards),'families',len(groups))

if __name__=='__main__':main()
