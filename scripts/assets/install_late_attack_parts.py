"""Install reviewed late mechanical/destroyed textures without repacking art."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
from functools import lru_cache
import sys,json,zlib
import numpy as np
from PIL import Image
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=128)
def pixels(i):return g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]]))
path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings']
plan=json.loads((OUT/'late_attack_sheets.json').read_text());inventory=json.loads((ROOT/'test_current/rom_catalog/animation_inventory.json').read_text())
active={b.get('index_hash') for b in bindings if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}
known={b['hash'] for b in bindings if b.get('rgb_enabled',True) and not b.get('disabled')};blocked=set(meta.get('indexed_collision_keys',[]));sources={};quality=[]
for sheet in plan['sheets']:
    image=OUT/sheet['image']
    if not image.exists():continue
    with Image.open(image) as im:
        assert im.mode=='RGBA';paint=np.asarray(im.resize((512,512),Image.Resampling.LANCZOS))[:,:,3]>64
    native=np.asarray(Image.open(OUT/(sheet['name']+'_native.png')))[:,:,3]>64
    iou=float((paint&native).sum()/max(1,(paint|native).sum()));assert iou>.55,(sheet['name'],iou)
    quality.append(dict(sheet=sheet['name'],alpha_iou=iou))
    meta['atlases'][sheet['name']]=dict(image='animation_parts/'+sheet['image'],reference='animation_parts/'+sheet['name']+'_native.png',native_size=[512,512],lazy=True)
    for segment in sheet['segments']:sources[segment['resource']]=(sheet['name'],segment)
added=0;registered=[]
for p in inventory['parts']:
    if p['image'] not in sources or p['index_hash'] in active or p['index_hash'] in blocked:continue
    name,s=sources[p['image']];a=pixels(p['image'])[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']];h,w=a.shape
    assert (w,h)==(p['w'],p['h'])
    indexed=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');assert zlib.crc32(indexed.tobytes())^(w<<16)^h==p['index_hash']
    pal=np.asarray(s['palette_rgb']);q=np.rint(pal*31/255).astype('uint16');colors=q[:,0]|(q[:,1]<<5)|(q[:,2]<<10)
    encoded=np.where(a,colors[a]|0x8000,0).astype('<u2');key=zlib.crc32(encoded.tobytes())^(w<<16)^h
    used=np.unique(a[a!=0]);unique=len(np.unique(pal[used],axis=0));safe=p['opaque']>=16 and unique>=3 and unique==len(used)
    if key in known and not safe:continue
    spec=dict(hash=key,rgb_enabled=key not in known,index_hash=p['index_hash'],x=s['x']+p['x'],y=s['y']+p['y'],w=w,h=h,atlas_id=name,auto_late_attack=True,resource=p['image'],source_x=p['x'],source_y=p['y'],dynamic_palette=True,indexed_safe=safe,original_palette_rgb=s['palette_rgb'])
    bindings.append(spec);registered.append(len(bindings));known.add(key)
    if safe:active.add(p['index_hash'])
    added+=1
assert len(bindings)<100000
path.write_text(json.dumps(meta,indent=2));result=dict(added_this_run=added,late_attack_bindings=sum(bool(b.get('auto_late_attack')) for b in bindings),generated_sheets=len(quality),source_images=len(sources),quality=quality,total_bindings=len(bindings),all_attacks_complete=False)
(OUT/'late_attack_installed.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
