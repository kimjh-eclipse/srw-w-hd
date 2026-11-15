"""Bring every arrived robot drawing up to "reviewed": split, fit/review, eye-review sheet.

For each unit with a drawing (SHEETS/sheet_NN/candidate_sheet.png, unified_sheet/
candidate_sheet.png, or COMBINED/candidate_combined.png) whose poses have not been
processed since the drawing changed: split into pose_NN/candidate.png, run
process_pose_drawings.py, write SHEET_REVIEW.png. Units already installed
(robot_set/INSTALLED) are skipped. Runs N units at a time.

  py -3.11 -X utf8 scripts/assets/ingest_drawings.py [--workers 6]
Prints one line per unit: accepted/rejected counts and the drawn resolution.
"""
import argparse,json,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

PY=[sys.executable,'-X','utf8']
BASE=ROOT/'test_current/parts/pose_packets'


def drawing_of(rs):
    sheets=sorted(rs.glob('SHEETS/sheet_*/candidate_sheet.png'))
    if sheets:return 'sheets',max(p.stat().st_mtime for p in sheets)
    for kind,p in (('combined',rs/'COMBINED/candidate_combined.png'),('unified',rs/'unified_sheet/candidate_sheet.png')):
        if p.exists():return kind,p.stat().st_mtime
    return None,0


def todo():
    out=[]
    for rs in sorted(BASE.glob('unit_*/robot_set'),key=lambda p:int(p.parent.name[5:])):
        if (rs/'INSTALLED').exists():continue
        kind,stamp=drawing_of(rs)
        if not kind:continue
        hold=rs/'HOLD_REDRAW'
        if hold.exists() and hold.stat().st_mtime>stamp:continue   # waiting for the redraw
        status=rs/'DRAWINGS_STATUS.json'
        if status.exists() and status.stat().st_mtime>stamp:continue
        out.append((rs,kind))
    return out


def work(item):
    rs,kind=item;u=rs.parent.name
    try:
        if kind=='sheets':r=subprocess.run(PY+['scripts/assets/pose_sheets.py','split',str(rs)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        elif kind=='combined':r=subprocess.run(PY+['scripts/assets/combined_pose_sheet.py','split',str(rs),'candidate_combined.png'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        else:r=subprocess.run(PY+['scripts/assets/split_unified_sheet.py',str(rs)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        if r.returncode:return f"{u} split failed: {(r.stderr or r.stdout).strip().splitlines()[-1:]}"
        res=[l for l in r.stdout.splitlines() if 'px per native' in l]
        subprocess.run(PY+['scripts/verify/drawing_resolution.py',u[5:],'--hold'],cwd=ROOT,capture_output=True)
        if (rs/'HOLD_REDRAW').exists() and (rs/'HOLD_REDRAW').stat().st_mtime>drawing_of(rs)[1]:
            return f"{u} {kind} held: drawn resolution below 2.5 px per native px (SHEETS built for redraw)"
        (rs/'DRAWINGS_STATUS.json').unlink(missing_ok=True)
        r=subprocess.run(PY+['scripts/assets/process_pose_drawings.py',str(rs)],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
        subprocess.run(PY+['scripts/verify/sheet_side_by_side.py',u[5:],'1800'],cwd=ROOT,capture_output=True)
        s=json.loads((rs/'DRAWINGS_STATUS.json').read_text(encoding='utf-8')) if (rs/'DRAWINGS_STATUS.json').exists() else {}
        acc=sum(v['state']=='accepted' for v in s.values())
        return f"{u} {kind} accepted {acc}/{len(s)} {res[0].split('->')[-1].strip() if res else ''}"
    except Exception as e:return f"{u} error {e}"


def main():
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=6);a=p.parse_args()
    items=todo();print('units to ingest',len(items),flush=True)
    with ThreadPoolExecutor(a.workers) as ex:
        for line in ex.map(work,items):print(line,flush=True)
    print('INGEST DONE',flush=True)


if __name__=='__main__':main()
