"""Install observed cut-in identities and exact dialogue portrait identities."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json
import numpy as np
from PIL import Image
from hd_parts_registration import register_part
ROOT=PROJECT_ROOT;OUT=ROOT/'graphics/portraits';SOURCE=ROOT/'test_current/attract'
plan=json.loads((OUT/'observed.json').read_text());cutins=[];portraits=[]
for n,source in enumerate(plan['cutins'],2):
    image=OUT/source['image']
    if not image.exists():continue
    native=Image.open(OUT/(source['name']+'_native.png')).convert('RGBA');paint=Image.open(image).convert('RGBA')
    a=np.asarray(paint.resize(native.size,Image.Resampling.LANCZOS))[:,:,3]>64;b=np.asarray(native)[:,:,3]>64
    iou=float((a&b).sum()/max(1,(a|b).sum()));assert iou>.65,(source['name'],iou)
    registered,stats=register_part(paint,native);target=source['name']+'_registered.png';registered.save(OUT/target)
    frames=[7040,7080] if source['name']=='gauron_body' else [8100,8130];hashes=[]
    for frame in frames:
        data=np.load(SOURCE/f'bg_{frame}_1.npz');entry=int.from_bytes(data['map'].tobytes()[:2],'little')&1023
        raw=data['tiles'].tobytes()[entry*32+1024:entry*32+3072];assert len(raw)==2048
        h=2166136261
        for value in raw:h=((h^value)*16777619)&0xffffffff
        hashes.append(h)
    cutins.append(dict(id=n,name=source['name'],layer=1,native_size=source['native_size'],image='portraits/'+target,signatures=sorted(set(hashes)),alpha_iou=iou,registration=stats))
for source in plan['portraits']:
    if not (OUT/source['image']).exists():continue
    portraits.append(dict(**source,path='portraits/'+source['image']))
(ROOT/'graphics/cutins_library.json').write_text(json.dumps(dict(cutins=cutins),indent=2))
# Portrait installation also includes all generated archive sheets.
from scripts.assets.install_portraits import main as install_all_portraits
install_all_portraits()
print(json.dumps(dict(cutins=len(cutins),portraits=len(json.loads((OUT/'library.json').read_text())['portraits']))))
