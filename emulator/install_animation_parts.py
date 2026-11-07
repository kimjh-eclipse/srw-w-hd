"""Append verified new basic fragments, preserving every approved binding ID."""
from pathlib import Path
import json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/animation_parts'
plan=json.loads((OUT/'basic_extra_sheets.json').read_text());path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings']
oldplan=json.loads((ROOT/'graphics/all_units/batches.json').read_text());duplicates={p['resource']:p['source'] for p in oldplan['duplicates']}
sources={s['resource']:("all_"+b['name'],s['batch_y']) for b in oldplan['batches'] if b.get('required') for s in b['segments']}
known={b['hash'] for b in bindings if b.get('rgb_enabled',True)};added=0;quality=[]
for sheet in plan['sheets']:
    target=OUT/sheet['image'];key=sheet['name'];has_image=target.exists()
    if has_image:
        meta['atlases'][key]=dict(image='animation_parts/'+sheet['image'],reference='animation_parts/'+sheet['name']+'_native.png',native_size=[256,256],lazy=True)
        art=np.array(Image.open(target).convert('RGBA').resize((256,256),Image.Resampling.LANCZOS))[:,:,3]>64
        native=np.array(Image.open(OUT/(sheet['name']+'_native.png')))[:,:,3]>64
        iou=float((art&native).sum()/max(1,(art|native).sum()));quality.append(dict(sheet=key,alpha_iou=iou))
        assert iou>.55,(key,'generated layout deviated',iou)
    for p in sheet['parts']:
        if p['hash'] in known:continue
        if has_image:atlas=key;x=p['atlas_x'];y=p['atlas_y']
        else:
            # The final two 8x8 slivers already exist in approved full atlases.
            source=duplicates.get(p['image'],p['image']);assert source in sources,(key,p['image'],'HD image still pending')
            atlas,dy=sources[source];x=p['x'];y=p['y']+dy
        bindings.append(dict(hash=p['hash'],index_hash=p['index_hash'],x=x,y=y,w=p['w'],h=p['h'],atlas_id=atlas,auto_animation=True,resource=p['image'],dynamic_palette=True,indexed_safe=p['opaque']>=16,original_palette_rgb=p['palette_rgb']))
        known.add(p['hash']);added+=1
# Resource 7406 is a pilot eye strip, not a robot. Retain its IDs for old
# metadata references but exclude it from both native match tables.
for b in bindings:
    if b.get('auto_unit') and b.get('resource')==7406:b.update(disabled=True,disabled_reason='pilot_eye_strip')
path.write_text(json.dumps(meta,indent=2))
result=dict(new_basic_parts=plan['parts'],added=added,total_bindings=len(bindings),quality=quality,all_attacks_complete=False)
(OUT/'installed.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
