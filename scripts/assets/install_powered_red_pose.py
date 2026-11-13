"""Connect all nine freshly painted parts of the observed Powered Red pose."""
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

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets.audit_missing_parts import decode


def main():
    p=argparse.ArgumentParser();p.add_argument('--drawing',type=Path,required=True)
    p.add_argument('--apply',action='store_true');args=p.parse_args()
    cap=ROOT/'test_current/combat/named_attacks/unit_99/diagnostic_preview/weapon_415_capture'
    contract=json.loads((ROOT/'test_current/parts/powered_red/pose_atlas_contract.json').read_text())
    objects=json.loads((cap/'obj_1320.json').read_text())
    libpath=ROOT/'graphics/kazuma_parts_library.json'
    lib=json.loads(libpath.read_text(encoding='utf-8'))
    protected=hashlib.sha256(json.dumps(lib['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    drawing=Image.open(args.drawing).convert('RGBA')
    native_atlas=Image.new('RGBA',(144,144));atlas=Image.new('RGBA',(576,576))
    name='powered_red_pose_reviewed';records=[]
    with np.load(cap/'obj_1320.npz') as data:
        disp=int.from_bytes(data['regs'][:4].tobytes(),'little')
        for i,c in enumerate(contract):
            obj=next(o for o in objects if o['hash']==c['hash'])
            key,ikey,idx,native,_,colors=decode(data['vram'].tobytes(),
                data['palette'][512:1024].tobytes(),obj['a'],obj['b'],obj['c'],disp)
            assert key==c['hash'] and ikey==c['index_hash']
            x,y,w,h=c['box'];native_atlas.alpha_composite(native,(x,y))
            cell=drawing.crop((round(i%3*drawing.width/3),round(i//3*drawing.height/3),
                round((i%3+1)*drawing.width/3),round((i//3+1)*drawing.height/3)))
            bb=cell.getchannel('A').point(lambda a:255 if a>64 else 0).getbbox()
            target=native.getbbox();part=Image.new('RGBA',(w*4,h*4))
            part.alpha_composite(cell.crop(bb).resize(((target[2]-target[0])*4,
                (target[3]-target[1])*4),Image.Resampling.LANCZOS),(target[0]*4,target[1]*4))
            expected=np.asarray(native.getchannel('A'))>64
            actual=np.asarray(part.getchannel('A').resize((w,h),Image.Resampling.BOX))>64
            iou=float((expected&actual).sum()/(expected|actual).sum())
            assert iou>=.78,(i,iou)
            atlas.alpha_composite(part,(x*4,y*4))
            rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,
                ((colors>>10)&31)*255//31],-1).astype('uint8').tolist()
            existing=next((j for j,b in enumerate(lib['bindings'])
                if b['hash']==key and b.get('rgb_enabled',True)),None)
            if existing is not None:
                assert lib['bindings'][existing].get('atlas_id') in (name,'powered_red_head_reviewed')
            spec=dict(hash=key,index_hash=ikey,rgb_enabled=True,indexed_safe=False,
                dynamic_palette=True,original_palette_rgb=rgb,
                index_pixels=base64.b64encode(zlib.compress(idx.tobytes())).decode(),
                x=x,y=y,w=w,h=h,atlas_id=name,registered_attack_bank=True,
                preserve_canonical_paint=True,reviewed_unit=99,reviewed_weapon=415,
                observed_native_rectangle=True,observed_complete=True)
            if existing is None:lib['bindings'].append(spec);identifier=len(lib['bindings'])
            else:lib['bindings'][existing]=spec;identifier=existing+1
            records.append(dict(slot=i,binding=identifier,hash=key,alpha_iou=iou))
    assert len(records)==9
    assert protected==hashlib.sha256(json.dumps(lib['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply:
        folder=ROOT/'graphics/rework_powered_red';folder.mkdir(exist_ok=True)
        shutil.copy2(args.drawing,folder/'pose_generated.png')
        atlas.save(folder/'pose_hd.png');native_atlas.save(folder/'pose_native.png')
        lib['atlases'][name]=dict(image='rework_powered_red/pose_hd.png',
            reference='rework_powered_red/pose_native.png',native_size=[144,144],lazy=True)
        tmp=libpath.with_suffix('.tmp.json');tmp.write_text(json.dumps(lib,indent=2),encoding='utf-8');tmp.replace(libpath)
    report=dict(parts=records,applied=args.apply,source_palette='captured frame 1320',
        indexed_bindings_unchanged=True,all_weapons_complete=False,gameplay_verified=False)
    (ROOT/'test_current/parts/powered_red/pose_install.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))


if __name__=='__main__':main()
