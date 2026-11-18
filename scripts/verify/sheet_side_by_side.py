"""Native sheet | drawn sheet side by side (on grey) for eye review of a unit's drawing.

Handles 9-pose SHEETS (one row per sheet, stacked), COMBINED and unified_sheet.

  py -3.11 -X utf8 scripts/verify/sheet_side_by_side.py <unit number> [max width]
writes <set>/SHEET_REVIEW.png
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image

GREY=(80,82,92,255)


def pair(nat,can):
    a=Image.open(nat).convert('RGBA');b=Image.open(can).convert('RGBA').resize(a.size)
    W,H=a.size;out=Image.new('RGBA',(W*2+24,H),GREY)
    for k,im in enumerate((a,b)):
        bg=Image.new('RGBA',im.size,GREY);bg.alpha_composite(im);out.paste(bg,(k*(W+24),0))
    return out


def main():
    u=int(sys.argv[1]);mw=int(sys.argv[2]) if len(sys.argv)>2 else 1800
    rs=ROOT/f'test_current/parts/pose_packets/unit_{u}/robot_set'
    # The assembled sheet holds the poses actually cut (newest Codex repair wins); the official sheet only when none.
    sheets=[max((c for c in (s/'candidate_sheet_assembled.png',s/'candidate_sheet.png') if c.exists()),key=lambda c:c.stat().st_mtime) for s in sorted(rs.glob('SHEETS/sheet_*')) if (s/'candidate_sheet.png').exists() or (s/'candidate_sheet_assembled.png').exists()]
    if sheets:
        rows=[pair(c.parent/'native_sheet_4x.png',c) for c in sheets]
        W=max(r.width for r in rows);out=Image.new('RGBA',(W,sum(r.height+24 for r in rows)),(40,40,48,255));y=0
        for r in rows:out.paste(r,(0,y));y+=r.height+24
    elif u==2 and (rs/'COMBINED/candidate_combined.png').exists():out=pair(rs/'COMBINED/native_combined_4x.png',rs/'COMBINED/candidate_combined.png')
    else:
        sh=rs/'unified_sheet'
        nat=next((p for p in sorted(sh.glob('native*.png')) if 'preview' not in p.name),None)
        out=pair(nat,sh/'candidate_sheet.png')
    out.thumbnail((mw,mw*3));out.save(rs/'SHEET_REVIEW.png');print(rs/'SHEET_REVIEW.png',out.size)


if __name__=='__main__':main()
