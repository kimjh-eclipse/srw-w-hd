"""Create compact visual QA pages of completed portrait atlas sheets."""
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent;SHEETS=ROOT/'graphics/portraits/sheets';OUT=ROOT/'test_current/portrait'
for start in range(0,34,6):
    sheet=Image.new('RGB',(1536,936),'#18202a');draw=ImageDraw.Draw(sheet)
    for k,n in enumerate(range(start,min(start+6,34))):
        path=SHEETS/f'portraits_{n:02}_hd.png'
        if not path.exists():continue
        with Image.open(path) as source:im=source.convert('RGBA').resize((512,448))
        x=k%3*512;y=k//3*468;sheet.paste(im,(x,y),im);draw.text((x,y+448),f'sheet {n:02}',fill='white')
    sheet.save(OUT/f'generated_sheets_{start//6:02}.png')
