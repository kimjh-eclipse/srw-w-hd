"""Bring Codex's full-robot redraw deliveries (full_robot_redraw_<date>/unit_N) into the robot sets.

Three index formats (11/20): unit_3 UNIT3_PREFERRED_TARGET_MAP.json (targets: pose -> raw_path/layout_path),
unit_4 UNIT4_FULL_REDRAW_INDEX.json (items: saved_raw_path/layout_snapshot/targets),
unit_5 UNIT5_PREFERRED_TARGET_MAP.json (targets: [pose/raw/layout]). Every pose uses its OWN layout.
The RAW is scaled to the layout's sheet size, the pose box (sheet_origin, source_canvas) is cut and
scaled to the pose's 4x canvas (native.png x4) -> robot_set/<pose>/candidate.png (old kept as
candidate_pre<date>.png). Codex RAWs have interior alpha 252/253: alpha >= 240 becomes 255 (the
outline keeps its soft alpha). Held poses are skipped. Then process_pose_drawings runs (fit/review).

  py -3.11 -X utf8 scripts/assets/ingest_full_redraw.py --root test_current/parts/full_robot_redraw_20261120 --units 3,4,5 --skip 5:pose_03
"""
import argparse,json,subprocess,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets'


def targets(ud,u):
    out=[]
    f=ud/f'UNIT{u}_PREFERRED_TARGET_MAP.json'
    if f.exists():
        m=json.loads(f.read_text(encoding='utf-8'));t=m['targets']
        if isinstance(t,dict):out=[(p,v.get('raw_path') or v.get('raw'),v.get('layout_path') or v.get('layout')) for p,v in t.items()]
        else:out=[(v['pose'],v.get('raw') or v.get('raw_path'),v.get('layout') or v.get('layout_path')) for v in t]
    f=ud/f'UNIT{u}_FULL_REDRAW_INDEX.json'
    if not out and f.exists():
        for it in json.loads(f.read_text(encoding='utf-8'))['items']:
            for p in it['targets']:out.append((p,it['saved_raw_path'],it['layout_snapshot']))
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--root',required=True);p.add_argument('--units',required=True);p.add_argument('--skip',default='');p.add_argument('--tag',default='20261120');p.add_argument('--no-process',action='store_true')
    a=p.parse_args();root=ROOT/a.root;skip=set(a.skip.split(',')) if a.skip else set()
    for u in map(int,a.units.split(',')):
        rs=BASE/f'unit_{u}/robot_set';done=[];missing=[]
        for pose,raw,lay in targets(root/f'unit_{u}',u):
            if f'{u}:{pose}' in skip:continue
            folder=rs/pose
            if not (folder/'native.png').exists():missing.append(pose);continue
            L=json.loads(Path(lay).read_text(encoding='utf-8'));e=next(x for x in L['layout'] if x['pose']==pose)
            ox,oy=e['sheet_origin'][:2];cw,ch=e['source_canvas']
            sheet=Image.open(raw).convert('RGBA').resize(tuple(L['sheet']),Image.Resampling.LANCZOS)
            crop=sheet.crop((ox,oy,ox+cw,oy+ch))
            nw,nh=Image.open(folder/'native.png').size
            if crop.size!=(nw*4,nh*4):crop=crop.resize((nw*4,nh*4),Image.Resampling.LANCZOS)
            arr=np.asarray(crop).copy();arr[...,3]=np.where(arr[...,3]>=240,255,arr[...,3]);arr[arr[...,3]==0,:3]=0
            old=folder/'candidate.png'
            if old.exists() and not (folder/f'candidate_pre{a.tag}.png').exists():old.rename(folder/f'candidate_pre{a.tag}.png')
            Image.fromarray(arr).save(folder/'candidate.png');done.append(pose)
        print('unit',u,'poses',len(done),'missing folders',missing,flush=True)
        (rs/f'FULL_REDRAW_{a.tag}.json').write_text(json.dumps(dict(root=a.root,poses=done,skipped=sorted(skip)),indent=1),encoding='utf-8')
        if a.no_process or not done:continue
        for f in ('DRAWINGS_STATUS.json','EYE_REVIEW.json','EYE_REVIEW_PENDING'):(rs/f).unlink(missing_ok=True)
        r=subprocess.run([sys.executable,'-X','utf8','scripts/assets/process_pose_drawings.py',str(rs)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        subprocess.run([sys.executable,'-X','utf8','scripts/verify/sheet_side_by_side.py',str(u),'1800'],cwd=ROOT,capture_output=True)
        s=json.loads((rs/'DRAWINGS_STATUS.json').read_text(encoding='utf-8')) if (rs/'DRAWINGS_STATUS.json').exists() else {}
        print('unit',u,'accepted',sum(v['state']=='accepted' for v in s.values()),'/',len(s),(r.stderr or '').strip().splitlines()[-1:] ,flush=True)


if __name__=='__main__':main()
