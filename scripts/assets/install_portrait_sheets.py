"""Crop generated atlas cells and register exact 5-bit native face identities."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageChops,ImageFilter
ROOT=PROJECT_ROOT;OUT=ROOT/'graphics/portraits';SHEETS=OUT/'sheets'
def main():
    plans=json.loads((SHEETS/'plan.json').read_text())['sheets'];items=[];reviews=[]
    hud=Image.open(ROOT/'test_current/robot/native_65040.png').convert('RGBA').crop((0,136,56,184))
    for plan in plans:
        path=SHEETS/(plan['name']+'_hd.png')
        if not path.exists():continue
        with Image.open(path) as source:paint=source.convert('RGBA')
        nw,nh=plan['native_size'];sx=paint.width/nw;sy=paint.height/nh
        assert abs(sx/sy-1)<.035,(plan['name'],paint.size)
        for item in plan['items']:
            x,y,w,h=item['rectangle'];art=paint.crop((round(x*sx),round(y*sy),round((x+w)*sx),round((y+h)*sy))).resize((448,384),Image.Resampling.LANCZOS)
            native=Image.open(OUT/item['path']).convert('RGBA')
            a=np.asarray(art.getchannel('A').resize((w,h),Image.Resampling.BOX))>64;b=np.asarray(native.getchannel('A'))>64
            iou=float((a&b).sum()/max(1,(a|b).sum()))
            assert iou>.60,(item['name'],iou)
            # Pin transparent scanline gaps and portrait cutouts to the original.
            contract=native.getchannel('A').resize(art.size,Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(.35))
            art.putalpha(ImageChops.multiply(art.getchannel('A'),contract))
            destination=f"archive/{item['name']}_hd.png";art.save(OUT/destination)
            composed=Image.alpha_composite(hud,native).convert('RGB');composed.save(OUT/(item['name']+'_native.png'))
            items.append(dict(name=item['name'],archive_img=item['img'],archive_plt=item['plt'],rectangle=[0,136,56,48],native_size=[56,48],crc32=zlib.crc32(composed.tobytes()),image=destination,match_format='rgb5',sheet=plan['name']))
            reviews.append(dict(name=item['name'],sheet=plan['name'],alpha_iou=round(iou,4)))
    (OUT/'observed_archive.json').write_text(json.dumps(dict(portraits=items),indent=2))
    (ROOT/'test_current/portrait/sheet_validation.json').write_text(json.dumps(dict(portraits=reviews),indent=2))
    print(json.dumps(dict(portraits=len(items),sheets=len(set(x['sheet'] for x in items)))))
if __name__=='__main__':main()
