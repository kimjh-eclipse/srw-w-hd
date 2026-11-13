"""Install a newly painted head for an observed Powered Red RGB identity.

Never steals an indexed binding shared with another unit/palette. The exact
captured native texture and palette are retained with the new artwork.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import shutil
import sys
import zlib

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets.audit_missing_parts import decode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--drawing', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    capture = ROOT/'test_current/combat/named_attacks/unit_99/diagnostic_preview/weapon_415_capture'
    objects = json.loads((capture/'obj_1320.json').read_text())
    obj = next(o for o in objects if o['hash'] == 3682593579)
    with np.load(capture/'obj_1320.npz') as data:
        disp = int.from_bytes(data['regs'][:4].tobytes(), 'little')
        key, ikey, indices, native, _, colors = decode(
            data['vram'].tobytes(), data['palette'][512:1024].tobytes(),
            obj['a'], obj['b'], obj['c'], disp)
    assert key == obj['hash'] and ikey == obj['index_hash']
    painting = Image.open(args.drawing).convert('RGBA')
    visible = painting.getchannel('A').point(lambda a: 255 if a > 64 else 0).getbbox()
    box = native.getbbox()
    atlas = Image.new('RGBA', (native.width*4, native.height*4))
    atlas.alpha_composite(painting.crop(visible).resize(
        ((box[2]-box[0])*4, (box[3]-box[1])*4), Image.Resampling.LANCZOS),
        (box[0]*4, box[1]*4))
    expected = np.asarray(native.getchannel('A')) > 64
    actual = np.asarray(atlas.getchannel('A').resize(native.size, Image.Resampling.BOX)) > 64
    iou = float((expected & actual).sum() / (expected | actual).sum())
    assert iou >= .78, f'Head silhouette drift: {iou}'
    library = ROOT/'graphics/kazuma_parts_library.json'
    meta = json.loads(library.read_text(encoding='utf-8'))
    protected = hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    rgb = np.stack([(colors&31)*255//31, ((colors>>5)&31)*255//31,
                    ((colors>>10)&31)*255//31], -1).astype('uint8').tolist()
    name = 'powered_red_head_reviewed'
    binding = dict(hash=key, index_hash=ikey, rgb_enabled=True, indexed_safe=False,
                   dynamic_palette=True, original_palette_rgb=rgb,
                   index_pixels=base64.b64encode(zlib.compress(indices.tobytes())).decode(),
                   x=0,y=0,w=native.width,h=native.height,atlas_id=name,resource=9416,
                   registered_attack_bank=True,preserve_canonical_paint=True,
                   reviewed_unit=99,reviewed_weapon=415)
    existing = next((i for i,b in enumerate(meta['bindings'])
                     if b.get('atlas_id')==name and b['hash']==key), None)
    assert not any(b['hash']==key and b.get('rgb_enabled',True)
                   for i,b in enumerate(meta['bindings']) if i!=existing)
    if existing is None:
        meta['bindings'].append(binding)
        identifier = len(meta['bindings'])
    else:
        meta['bindings'][existing] = binding
        identifier = existing + 1
    folder = ROOT/'graphics/rework_powered_red'
    if args.apply:
        folder.mkdir(exist_ok=True)
        shutil.copy2(args.drawing, folder/'head_generated.png')
        atlas.save(folder/'head_hd.png')
        native.save(folder/'head_native.png')
        meta['atlases'][name] = dict(image='rework_powered_red/head_hd.png',
            reference='rework_powered_red/head_native.png',native_size=list(native.size),lazy=True)
        assert protected == hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
        temp = library.with_suffix('.tmp.json')
        temp.write_text(json.dumps(meta,indent=2),encoding='utf-8')
        temp.replace(library)
    report = dict(binding=identifier,hash=key,index_hash=ikey,alpha_iou=iou,
                  applied=args.apply,indexed_binding_replaced=False,gameplay_verified=False)
    (ROOT/'test_current/parts/powered_red/head_install.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))


if __name__ == '__main__':
    main()
