"""Contact sheets for visual inspection of the assembled primary forms."""
from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageOps
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/all_units'
packages=[p for p in json.loads((OUT/'catalog.json').read_text())['packages'] if p['resource']<3500]
for page in range(math.ceil(len(packages)/30)):
    sheet=Image.new('RGB',(1440,1050),'#182334');draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(packages[page*30:page*30+30]):
        resource=p['resource'];art=Image.open(OUT/f'unit_{resource}_hd_pose.png').convert('RGBA');box=art.getbbox()
        if box:art=art.crop(box)
        art=ImageOps.contain(art,(228,180),Image.Resampling.LANCZOS)
        x=(i%6)*240+(240-art.width)//2;y=(i//6)*210+18
        sheet.paste(art,(x,y),art);draw.text(((i%6)*240+10,(i//6)*210+194),f'{page*30+i+1}: {resource}',fill='white')
    sheet.save(OUT/f'hd_review_{page:02}.png')
print(f'{len(packages)} assembled forms / {page+1} review sheets')
