"""Prepare exact observed cut-in maps and dialogue portraits for AI redraw."""
from pathlib import Path
import json,zlib
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent;SOURCE=ROOT/'test_current/attract';OUT=ROOT/'graphics/portraits';OUT.mkdir(exist_ok=True)
assets=[]
for name,frame in [('gauron_body',7040),('gauron_face',8100)]:
    im=Image.open(SOURCE/f'bg_{frame}_1.png').convert('RGBA').crop((0,0,256,192));a=np.array(im);a[a[:,:,3]==0,:3]=0;im=Image.fromarray(a)
    im.save(OUT/f'{name}_native.png');im.resize((1536,1152),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    assets.append(dict(name=name,frame=frame,layer=1,native_size=[256,192],image=f'{name}_hd.png'))
portraits=[];sheet=Image.new('RGB',(384,256),'#15212d');draw=ImageDraw.Draw(sheet)
for n,(name,frame) in enumerate([('mao',5910),('kurz',6030),('sousuke',6120),('gauron',6900),('gai',8800),('zondar',9900)]):
    im=Image.open(SOURCE/f'native_{frame}.png').convert('RGB').crop((0,136,56,184));im.save(OUT/f'{name}_native.png')
    mask=Image.new('L',im.size);ImageDraw.Draw(mask).polygon([(0,0),(48,0),(56,8),(56,48),(0,48)],fill=255)
    reference=im.convert('RGBA');reference.putalpha(mask);reference.resize((1008,864),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    sheet.paste(im.resize((96,96),Image.Resampling.NEAREST),(n%3*128,n//3*128));draw.text((n%3*128,n//3*128+98),name,fill='white')
    portraits.append(dict(name=name,frame=frame,rectangle=[0,136,56,48],native_size=[56,48],crc32=zlib.crc32(im.tobytes()),image=f'{name}_hd.png'))
sheet.save(OUT/'portrait_review.png');(OUT/'observed.json').write_text(json.dumps(dict(cutins=assets,portraits=portraits),indent=2))
