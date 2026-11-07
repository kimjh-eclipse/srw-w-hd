"""Native resource contact sheets for deciding actual mechanical art scope."""
from pathlib import Path
import sys,json,math,time
import numpy as np
from PIL import Image,ImageDraw,ImageOps
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts';OUT.mkdir(exist_ok=True)
inventory=json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text());audit=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text())
palettes={i:p['palette'] for p in audit['patterns'] for i in p['image_group']}
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
items=[p for p in inventory['image_stats'] if p['new_unique'] and p['image']>=4395]
for page in range(math.ceil(len(items)/48)):
    sheet=Image.new('RGB',(1792,960),'#182334');draw=ImageDraw.Draw(sheet)
    for cell,item in enumerate(items[page*48:page*48+48]):
        i=item['image'];indices=g.pixels(resource(i));palette=resource(palettes[i]);colors=np.array(g.palette(palette),dtype='uint8')
        if len(colors)<=int(indices.max()):colors=np.array([(j*17,j*17,j*17,255) for j in range(16)],dtype='uint8')
        image=colors[indices].copy();image[:,:,3]=np.where(indices,255,0);image[indices==0,:3]=0
        native=Image.fromarray(image);native.save(OUT/f'source_{i}.png');im=ImageOps.contain(native,(216,135),Image.Resampling.NEAREST)
        x=cell%8*224;y=cell//8*160;sheet.paste(im,(x+(224-im.width)//2,y+(140-im.height)//2),im)
        draw.text((x+4,y+142),f'{i}  known:{item["existing"]} new:{item["new_unique"]}',fill='white')
    sheet.save(OUT/f'review_{page:02}.png')
(OUT/'sources.json').write_text(json.dumps(dict(items=items,pages=page+1),indent=2));print(len(items),page+1)
