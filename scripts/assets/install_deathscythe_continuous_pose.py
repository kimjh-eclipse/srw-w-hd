"""Install only the three source rectangles painted as one OAM-aligned pose."""
import argparse, hashlib, json, shutil, sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--apply',action='store_true');parser.add_argument('--full-pose',action='store_true');args=parser.parse_args()
    folder=ROOT/'test_current/parts/deathscythe';candidate=folder/('full_candidate' if args.full_pose else 'candidate')
    geometry=json.loads((candidate/'report.json').read_text())
    assert geometry['lost_opaque_pixels']<=16, geometry
    contract=json.loads((folder/('full_pose_contract.json' if args.full_pose else 'pose_inverse_registration.json')).read_text())
    art=Image.open(candidate/'candidate_atlas.png').convert('RGBA')
    native=Image.open(ROOT/'graphics/rework_deathscythe/attack_7108_native.png').convert('RGBA')
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text())
    before=hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    name='deathscythe_7108_continuous';rows=[]
    for part in contract['parts']:
        binding=part['binding'];spec=meta['bindings'][binding-1]
        assert spec['resource']==7108 and spec['source_x']==part['source_x']
        x=part['source_x'];w=part['w'];h=part['h']
        expected=np.asarray(native.crop((x,0,x+w,h)).getchannel('A'))>64
        actual=np.asarray(art.crop((x*4,0,(x+w)*4,h*4)).getchannel('A').resize((w,h),Image.Resampling.BOX))>64
        iou=float((expected&actual).sum()/max(1,(expected|actual).sum()))
        assert iou>=.60,(binding,iou)
        rows.append(dict(binding=binding,alpha_iou=iou,previous_atlas=spec['atlas_id']))
        spec.update(atlas_id=name,x=x,y=0,registered_attack_bank=True,preserve_canonical_paint=True,
                    paint_review_source='rework_deathscythe/pose_repaint_generated.png')
    assert len(rows)==3
    assert before==hashlib.sha256(json.dumps(meta['bindings'][:5263],sort_keys=True).encode()).hexdigest()
    if args.apply:
        target=ROOT/'graphics/rework_deathscythe'
        shutil.copy2(folder/('full_pose_generated.png' if args.full_pose else 'pose_repaint_generated.png'),target/'pose_repaint_generated.png')
        art.save(target/'pose_continuous_hd.png')
        meta['atlases'][name]=dict(image='rework_deathscythe/pose_continuous_hd.png',reference='rework_deathscythe/attack_7108_native.png',native_size=[240,96],lazy=True)
        temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(meta,indent=2),encoding='utf-8');temp.replace(path)
    report=dict(applied=args.apply,atlas=name,parts=rows,geometry=geometry,original_prefix_preserved=True,
                other_107_resource_bindings_unchanged=True,all_weapons_complete=False)
    (folder/'continuous_install.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(json.dumps(report))

if __name__=='__main__':main()
