"""Drawn resolution of a unit's drawing: generated pixels per native pixel.

The sheet layout is in 4x native units; the generator's raw output size tells
how many pixels it really drew. Below --min (default 2.5) the drawing is too
coarse: the unit is put on hold (HOLD_REDRAW), its 9-pose SHEETS are built and
the unit is listed for Codex.

  py -3.11 -X utf8 scripts/verify/drawing_resolution.py 0 3 4 ... [--min 2.5] [--hold]
"""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image

BASE=ROOT/'test_current/parts/pose_packets'


def resolution(rs):
    sheets=sorted(rs.glob('SHEETS/sheet_*/candidate_sheet.png'))
    if sheets:
        vals=[]
        for c in sheets:
            lay=json.loads((c.parent/'layout.json').read_text(encoding='utf-8'));g=c.parent/'generated_sheet.png'
            w=Image.open(g if g.exists() else c).width;vals.append(4*w/lay['sheet'][0])
        return min(vals)
    for folder,lay_name,gen in (('unified_sheet','source_layout.json','generated_all_poses.png'),('COMBINED','layout.json','generated_combined.png')):
        f=rs/folder/lay_name
        if not f.exists():continue
        L=json.loads(f.read_text(encoding='utf-8'))
        s=L.get('sheet') if isinstance(L.get('sheet'),list) else L.get('sheet_size') or L.get('size') or L.get('source_sheet_size') or L.get('canvas')
        g=rs/folder/gen
        if not g.exists():g=next(iter(sorted((rs/folder).glob('generated*.png'))),None)
        if g is None:g=rs/folder/('candidate_sheet.png' if folder=='unified_sheet' else 'candidate_combined.png')
        return 4*Image.open(g).width/s[0]
    return None


def main():
    p=argparse.ArgumentParser();p.add_argument('units',nargs='+',type=int);p.add_argument('--min',type=float,default=2.5);p.add_argument('--hold',action='store_true')
    a=p.parse_args();low=[]
    for u in a.units:
        rs=BASE/f'unit_{u}/robot_set';r=resolution(rs)
        print(u,'px per native',None if r is None else round(r,2))
        if r is not None and r<a.min:
            low.append((u,round(r,2)))
            if a.hold:
                (rs/'HOLD_REDRAW').write_text(f'drawn at {r:.2f} px per native px (< {a.min}); redraw on SHEETS (9 poses per sheet)\n',encoding='utf-8')
                (rs/'EYE_REVIEW_PENDING').unlink(missing_ok=True)
                if not (rs/'SHEETS').exists():subprocess.run([sys.executable,'-X','utf8','scripts/assets/pose_sheets.py','build',str(rs)],cwd=ROOT,capture_output=True)
    print('LOW',low)


if __name__=='__main__':main()
