"""Connect the reviewed named-unit fragment atlases without replacing IDs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
import json,zlib,base64,hashlib
import numpy as np
from PIL import Image

def main():
    folder=ROOT/'graphics/named_variants';plan=json.loads((folder/'plan.json').read_text(encoding='utf-8'))
    path=ROOT/'graphics/kazuma_parts_library.json';lib=json.loads(path.read_text());bindings=lib['bindings']
    prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    known={b['hash'] for b in bindings if b.get('rgb_enabled',True) and not b.get('disabled')}
    blocked=set(lib.get('indexed_collision_keys',[]))
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    records=[];quality=[]
    for sheet in plan['sheets']:
        with Image.open(folder/sheet['image']) as paint:
            assert paint.mode=='RGBA' and max(paint.size)<=960
            alpha=np.asarray(paint.resize((256,256),Image.Resampling.BOX))[:,:,3]>64
        native=np.asarray(Image.open(folder/(sheet['name']+'_native.png')))[:,:,3]>64
        iou=float((alpha&native).sum()/max(1,(alpha|native).sum()));assert iou>.7,(sheet['name'],iou)
        quality.append(dict(sheet=sheet['name'],alpha_iou=iou))
        lib['atlases'][sheet['name']]=dict(image='named_variants/'+sheet['image'],reference='named_variants/'+sheet['name']+'_native.png',native_size=[256,256],lazy=True)
        for p in sheet['segments']:
            if p['hash'] in known:continue
            raw=g.decompress(rom[g.BASE+offsets[p['image']]:g.BASE+offsets[p['image']+1]])
            a=g.pixels(raw)[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
            ih=zlib.crc32(np.where(a,a.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(p['w']<<16)^p['h']
            assert ih==p['index_hash']
            spec=dict(hash=p['hash'],index_hash=ih,rgb_enabled=True,indexed_safe=ih not in blocked and p['opaque']>=16 and len(np.unique(a[a!=0]))>=3,
                      x=p['atlas_x'],y=p['atlas_y'],w=p['w'],h=p['h'],atlas_id=sheet['name'],
                      resource=p['image'],source_x=p['x'],source_y=p['y'],auto_unit=True,auto_named_variant=True,
                      dynamic_palette=True,original_palette_rgb=p['palette_rgb'],unit_ids=p['unit_ids'],
                      index_pixels=base64.b64encode(zlib.compress(a.tobytes())).decode('ascii'),preserve_canonical_paint=True)
            bindings.append(spec);known.add(p['hash']);records.append(dict(binding=len(bindings),resource=p['image'],unit_ids=p['unit_ids']))
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    if records:
        tmp=path.with_suffix('.tmp.json');tmp.write_text(json.dumps(lib,indent=2));tmp.replace(path)
    report=dict(added=len(records),quality=quality,approved_prefix_preserved=True,bindings=records)
    (folder/'installed.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='bindings'}))

if __name__=='__main__':main()
