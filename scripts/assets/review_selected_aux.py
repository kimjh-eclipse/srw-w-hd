
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageOps
ROOT=PROJECT_ROOT;OUT=ROOT/'graphics/all_units'
plan=json.loads((OUT/'batches.json').read_text());ids=[i for i in plan['selected_resources'] if i>=3500]
image=Image.new('RGB',(1536,((len(ids)+5)//6)*120),'#182334');draw=ImageDraw.Draw(image)
for n,i in enumerate(ids):
    native=Image.open(OUT/f'unit_{i}_native.png').convert('RGBA');native=ImageOps.contain(native,(248,95),Image.Resampling.NEAREST)
    x=n%6*256;y=n//6*120;image.paste(native,(x,y),native);draw.text((x,y+100),str(i),fill='white')
image.save(ROOT/'test_current/rom_catalog/selected_aux_review.png')
