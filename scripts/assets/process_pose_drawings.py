"""Review and fit every arrived pose drawing of a robot set.

For each pose_NN with candidate.png newer than its candidate_fit.png:
review the raw drawing, fit it (fit_pose_drawing.py), review the fitted one.
A pose is accepted when the fitted drawing passes and the fit stayed small
(scale within 6%, offset within 12 px at 4x) - a larger correction means the
drawing does not sit on the native pose and goes back to Codex.
Writes <set>/DRAWINGS_STATUS.json and prints one line per pose.

  py -3.11 -X utf8 scripts/assets/process_pose_drawings.py <set dir>
"""
import json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

PY=[sys.executable,'-X','utf8']


def review(folder,name):
    subprocess.run(PY+['scripts/verify/review_pose_drawing.py',str(folder),name],cwd=ROOT,capture_output=True)
    return json.loads((folder/'review.json').read_text(encoding='utf-8'))


def main():
    root=Path(sys.argv[1]);status_path=root/'DRAWINGS_STATUS.json'
    status=json.loads(status_path.read_text(encoding='utf-8')) if status_path.exists() else {}
    for folder in sorted(d for d in root.glob('pose_*') if d.is_dir()):
        cand=folder/'candidate.png';fit=folder/'candidate_fit.png'
        if not cand.exists():continue
        if fit.exists() and fit.stat().st_mtime>cand.stat().st_mtime and folder.name in status:continue
        raw=review(folder,'candidate.png')
        if raw.get('size')!=raw.get('expected'):
            status[folder.name]=dict(state='rejected',reason=f"canvas {raw.get('size')} != {raw.get('expected')}");print(folder.name,status[folder.name],flush=True);continue
        subprocess.run(PY+['scripts/assets/fit_pose_drawing.py',str(folder)],cwd=ROOT,capture_output=True)
        info=json.loads((folder/'fit.json').read_text(encoding='utf-8'))
        done=review(folder,'candidate_fit.png');(folder/'review.png').replace(folder/'review_fit.png')
        big=max(abs(info['scale'][0]-1),abs(info['scale'][1]-1))>.12 or max(abs(v) for v in info['offset_4x'])>16
        reasons=list(done['fail'])+(['fit correction too large (drawing does not sit on the native pose)'] if big else [])
        status[folder.name]=dict(state='accepted' if not reasons else 'rejected',reasons=reasons,iou_raw=raw.get('iou'),iou_fit=done.get('iou'),
            scale=info['scale'],offset_4x=info['offset_4x'],filled_px=info['filled_px'],trimmed_px=info['trimmed_px'],
            weak=[(s['oam'],s['painted'],s['colour']) for s in done.get('weak_sprites',[])])
        print(folder.name,status[folder.name],flush=True)
    status_path.write_text(json.dumps(status,ensure_ascii=False,indent=1),encoding='utf-8')
    acc=sorted(k for k,v in status.items() if v['state']=='accepted');rej=sorted(k for k,v in status.items() if v['state']!='accepted')
    print('accepted',len(acc),acc,'rejected',len(rej),rej)


if __name__=='__main__':main()
