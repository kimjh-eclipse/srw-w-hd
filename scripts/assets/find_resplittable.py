"""Units whose poses lack candidate.png although a drawing for them now exists
(alternate layouts, aspect within 6%, unified sheets).

  py -3.11 -X utf8 scripts/assets/find_resplittable.py [--reset]
--reset clears DRAWINGS_STATUS / EYE_REVIEW / pending markers of those units (not the
INSTALLED marker) so the ingest loop splits, fits and sends them to eye review again.
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image
from scripts.assets.pose_sheets import drawing_sources

BASE=ROOT/'test_current/parts/pose_packets'


def coverable(rs):
    got=set()
    for official in sorted(rs.glob('SHEETS/sheet_*')):
        for cand,layf in drawing_sources(official):
            lay=json.loads(layf.read_text(encoding='utf-8'));W,H=lay['sheet']
            try:w,h=Image.open(cand).size
            except Exception:continue
            if abs((w/W)/(h/H)-1)>=.06:continue
            got|={e['pose'] for e in lay['layout']}
    return got


def main():
    p=argparse.ArgumentParser();p.add_argument('--reset',action='store_true');a=p.parse_args()
    out=[]
    for rs in sorted(BASE.glob('unit_*/robot_set'),key=lambda x:int(x.parent.name[5:])):
        if (rs/'HOLD_REDRAW').exists() or (rs/'CODEX_HOLD.txt').exists():continue
        missing={d.name for d in rs.glob('pose_*') if d.is_dir() and not (d/'candidate.png').exists()}
        if not missing:continue
        can=missing&coverable(rs)
        if can:out.append((rs.parent.name,len(can),(rs/'INSTALLED').exists()))
    for u,n,inst in out:print(u,'poses now cuttable',n,'(installed)' if inst else '')
    print('units',len(out),'poses',sum(n for _,n,_ in out))
    if a.reset:
        for u,_,_ in out:
            rs=BASE/u/'robot_set'
            for f in ('DRAWINGS_STATUS.json','EYE_REVIEW.json','EYE_REVIEW_PENDING','SHEET_REVIEW.png'):(rs/f).unlink(missing_ok=True)
        print('reset',len(out))


if __name__=='__main__':main()
