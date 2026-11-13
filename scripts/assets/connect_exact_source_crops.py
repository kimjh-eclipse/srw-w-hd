"""Connect source-confirmed crops from the same effect's existing artwork.

No recolouring, drawing, image duplication, or runtime change is performed.
Unobserved PAT/IMG/PLT contracts stay explicitly unobserved for the reviewer.
"""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import sys
import zlib

import numpy as np
from PIL import Image

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('contract',type=Path)
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    rows=json.loads(args.contract.read_text(encoding='utf-8'))
    path=ROOT/'graphics/kazuma_parts_library.json'
    meta=json.loads(path.read_text(encoding='utf-8'))
    prefix=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    known={r['hash']:i for i,r in enumerate(meta['bindings'],1) if r.get('rgb_enabled',True) and not r.get('disabled')}
    report=[]
    for r in rows:
        atlas=meta['atlases'][r['atlas_id']]
        live=ROOT/'graphics'/atlas['image']
        candidate=ROOT/r['candidate_file']
        assert live.read_bytes()==candidate.read_bytes(),('drawing provenance mismatch',r['hash'])
        art=Image.open(live).convert('RGBA')
        native=Image.open(ROOT/'graphics'/atlas['reference']).convert('RGBA')
        assert art.size==(native.width*4,native.height*4)
        assert atlas['native_size']==list(native.size)
        x,y,w,h=(int(r[k]) for k in ('x','y','w','h'))
        indices=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(h,w)
        mask=indices>0
        encoded=np.where(mask,indices.astype('uint16')|32768,0).astype('<u2')
        assert zlib.crc32(encoded.tobytes())^(w<<16)^h==r['index_hash']
        palette=np.asarray(r['palette_15bit'],dtype='uint16')
        encoded=np.where(mask,palette[indices]|32768,0).astype('<u2')
        assert zlib.crc32(encoded.tobytes())^(w<<16)^h==r['hash']
        reference=np.asarray(native.crop((x,y,x+w,y+h)))
        assert np.array_equal(reference[:,:,3]>0,mask)
        rgb=np.asarray(r['original_palette_rgb'],dtype=int)[indices]
        if mask.any():assert np.max(abs(reference[:,:,:3].astype(int)-rgb)[mask])<=1
        assert art.crop((x*4,y*4,(x+w)*4,(y+h)*4)).getchannel('A').getextrema()[1]>=16
        existing=known.get(r['hash'])
        if existing is not None:
            report.append(dict(hash=r['hash'],binding=existing,added=False))
            continue
        spec=dict(hash=r['hash'],index_hash=r['index_hash'],index_pixels=r['index_pixels'],
                  original_palette_rgb=r['original_palette_rgb'],x=x,y=y,w=w,h=h,
                  resource=r['source_image'],source_x=r['source_x'],source_y=r['source_y'],
                  atlas_id=r['atlas_id'],rgb_enabled=True,indexed_safe=False,dynamic_palette=False,
                  registered_attack_bank=True,preserve_canonical_paint=True,effect_part=bool(r.get('effect_part')),
                  reviewed_observed_pose=False,actual_observed=bool(r.get("actual_observed",False)),independent_visual_verification=False,
                  review_status='pending_claude',source_contract_status=r['source_contract_status'])
        meta['bindings'].append(spec)
        binding=len(meta['bindings']);known[r['hash']]=binding
        report.append(dict(hash=r['hash'],binding=binding,added=True,atlas=r['atlas_id'],actual_observed=bool(r.get('actual_observed',False))))
    assert prefix==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply:
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(meta,indent=2),encoding='utf-8');temp.replace(path)
    output=dict(applied=args.apply,parts=report,original_prefix_preserved=True,independent_visual_verification=False)
    args.contract.with_name('source_crop_install_report.json').write_text(json.dumps(output,indent=2),encoding='utf-8')
    print(json.dumps(output))


if __name__=='__main__':main()
