"""Append restored ROM part identities; preserve every existing approved ID."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,sys,hashlib
import numpy as np
from PIL import Image
ROOT=PROJECT_ROOT;OUT=ROOT/'graphics/all_units'
catalog=json.loads((OUT/'catalog.json').read_text());plan=json.loads((OUT/'batches.json').read_text())
path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];known={b['hash']:i for i,b in enumerate(bindings,1) if b.get('rgb_enabled',True)}
indexed_aliases={(b['index_hash'],b['source_binding'],json.dumps(b['original_palette_rgb'])) for b in bindings if b.get('rgb_enabled') is False}
duplicates={p['resource']:p['source'] for p in plan['duplicates']};lookup={};missing=[]
for batch in plan['batches']:
    if not batch.get('required',True):continue
    image=OUT/batch['image']
    if not image.exists():missing.append(batch['name']);continue
    key='all_'+batch['name']
    meta.setdefault('atlases',{})[key]=dict(image='all_units/'+batch['image'],reference='all_units/'+batch['reference'],native_size=batch['native_size'],lazy=True)
    for segment in batch['segments']:lookup[segment['resource']]=(key,segment['batch_y'])
if missing and '--partial' not in sys.argv:raise RuntimeError(f'{len(missing)} atlas images still pending')
coverage=[];added=0
for package in catalog['packages']:
    resource=package['resource'];canonical=duplicates.get(resource,resource)
    if resource in plan['excluded']:continue
    if canonical not in lookup:continue
    atlas,y=lookup[canonical];mapped=[]
    native=np.array(Image.open(OUT/f'unit_{resource}_native.png').convert('RGBA'))
    for part in package['parts']:
        key=part['hash']
        patch=native[part['y']:part['y']+part['h'],part['x']:part['x']+part['w']]
        opaque=patch[:,:,3]>0
        safe=int(opaque.sum())>=16 and len(np.unique(patch[:,:,:3][opaque],axis=0))>=3
        if key not in known:
            bindings.append(dict(hash=key,index_hash=part['index_hash'],indexed_safe=safe,x=part['x'],y=y+part['y'],w=part['w'],h=part['h'],atlas_id=atlas,auto_unit=True,resource=resource,dynamic_palette=True,original_palette_rgb=package['palette_rgb']))
            known[key]=len(bindings);added+=1
        elif bindings[known[key]-1].get('auto_unit'):bindings[known[key]-1]['indexed_safe']=safe
        mapped.append(known[key])
        base=bindings[known[key]-1];source_id=known[key]
        signature=(part['index_hash'],source_id,json.dumps(package['palette_rgb']))
        if safe and not base.get('source_binding') and signature not in indexed_aliases:
            if not base.get('dynamic_palette') or base.get('index_hash')!=part['index_hash'] or base['original_palette_rgb']!=package['palette_rgb']:
                bindings.append(dict(hash=key,rgb_enabled=False,index_hash=part['index_hash'],indexed_safe=True,source_binding=source_id,x=base['x'],y=base['y'],w=base['w'],h=base['h'],auto_unit=True,resource=resource,dynamic_palette=True,original_palette_rgb=package['palette_rgb']))
                indexed_aliases.add(signature);added+=1
    coverage.append(dict(resource=resource,bindings=mapped))
path.write_text(json.dumps(meta,indent=2))
report=dict(packages=len(coverage),parts=sum(len(p['bindings']) for p in coverage),added=added,total_bindings=len(bindings),missing_images=missing,coverage=coverage)
(OUT/'installed.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='coverage'}))
