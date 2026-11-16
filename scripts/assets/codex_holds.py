"""Codex 'do not install' markers for a robot set.

A drawing is held when Codex marked it, newer than (or at the same time as) the
drawing it applies to:
  unified_sheet/STYLE_REJECTION_HOLD.flag, unified_sheet/STYLE_REJECTED.txt
  SHEETS/STYLE_REWORK_HOLD.json (status *do_not_apply*), SHEETS/sheet_NN/STYLE_REJECTED.txt
  any STYLE_VERSION.json with do_not_install true, or a review_status containing
  'reject' or 'hold'.

  py -3.11 -X utf8 scripts/assets/codex_holds.py [unit ...]   (default: all units)
"""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

BASE=ROOT/'test_current/parts/pose_packets'


def holds(rs):
    out=[]
    def drawing_time(folder):
        c=[p for p in folder.glob('candidate*.png')]
        return max((p.stat().st_mtime for p in c),default=0)
    # Markers on the one-piece sheet do not apply once 9-pose SHEETS drawings
    # (the version in use) exist.
    uses_sheets=any(rs.glob('SHEETS/sheet_*/candidate_sheet.png'))
    unified=[] if uses_sheets else list(rs.glob('unified_sheet/STYLE_REJECTION_HOLD.flag'))+list(rs.glob('unified_sheet/STYLE_REJECTED.txt'))
    for f in unified+list(rs.glob('SHEETS/sheet_*/STYLE_REJECTED.txt')):
        if f.stat().st_mtime>=drawing_time(f.parent)-1:out.append(str(f.relative_to(rs)).replace('\\','/'))
    if (rs/'CODEX_HOLD.txt').exists():out.append('CODEX_HOLD.txt')
    j=rs/'SHEETS/STYLE_REWORK_HOLD.json'
    if j.exists():
        try:
            for o in json.loads(j.read_text(encoding='utf-8')).get('outputs',[]):
                if 'do_not_apply' in str(o.get('status','')):out.append(f"SHEETS/{o.get('sheet')} rework hold")
        except Exception:out.append('SHEETS/STYLE_REWORK_HOLD.json')
    for f in rs.rglob('STYLE_VERSION.json'):
        try:d=json.loads(f.read_text(encoding='utf-8'))
        except Exception:continue
        st=str(d.get('review_status','')).lower()
        if d.get('do_not_install') is True or 'reject' in st or 'hold' in st:out.append(str(f.relative_to(rs)).replace('\\','/'))
    return sorted(set(out))


def main():
    units=[int(x) for x in sys.argv[1:]] or sorted(int(p.parent.name[5:]) for p in BASE.glob('unit_*/robot_set'))
    for u in units:
        rs=BASE/f'unit_{u}/robot_set'
        if not rs.exists():continue
        h=holds(rs)
        if h:print(u,'INSTALLED' if (rs/'INSTALLED').exists() else 'pending',h)


if __name__=='__main__':main()
