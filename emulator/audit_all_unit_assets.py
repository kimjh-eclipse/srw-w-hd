"""Check atlas layout/alpha and preserve approved assets during expansion."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/all_units'
plan=json.loads((OUT/'batches.json').read_text());meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
prefix=dict(bindings=5263,sha256=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True,separators=(',',':')).encode()).hexdigest(),face_sha256=sha(ROOT/'graphics/kazuma_parts_atlas_facefix.png'),rom_sha256=sha(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'))
stamp=OUT/'approved_prefix.json'
if not stamp.exists():stamp.write_text(json.dumps(prefix,indent=2))
assert json.loads(stamp.read_text())==prefix,'Approved base assets changed'
assert prefix['rom_sha256']=='0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478'
results=[];missing=[];selected=set(plan['selected_resources'])
for batch in plan['batches']:
    if not batch.get('required',True):continue
    path=OUT/batch['image']
    if not path.exists():missing.append(batch['name']);continue
    with Image.open(path) as im:
        assert im.mode=='RGBA',(path,'no alpha')
        actual=im.size;art=im.resize(tuple(batch['native_size']),Image.Resampling.LANCZOS)
    native=Image.open(OUT/batch['reference']).convert('RGBA').resize(tuple(batch['native_size']),Image.Resampling.NEAREST)
    a=np.array(art)[:,:,3]>64;b=np.array(native)[:,:,3]>64
    mask=np.zeros(b.shape,dtype=bool)
    for segment in batch['segments']:
        if segment['resource'] in selected:mask[segment['batch_y']:segment['batch_y']+segment['height'],:segment['width']]=True
    if not mask.any():continue
    union=((a|b)&mask).sum();iou=float(((a&b)&mask).sum()/max(1,union))
    results.append(dict(batch=batch['name'],image_size=actual,alpha_iou=round(iou,4),aspect_error=round(abs(actual[0]/actual[1]-batch['native_size'][0]/batch['native_size'][1]),4)))
result=dict(required=sum(b.get('required',True) for b in plan['batches']),ready=len(results),missing=missing,approved_prefix_preserved=True,atlases=results)
(OUT/'asset_audit.json').write_text(json.dumps(result,indent=2))
print(json.dumps(dict(ready=len(results),missing=missing,lowest_alpha_iou=sorted(results,key=lambda r:r['alpha_iou'])[:8])))
if '--partial' not in sys.argv:assert not missing,'HD atlases missing'
assert all(r['alpha_iou']>.6 for r in results),'Atlas layout/alpha deviated from source'
