"""Native sheet | drawn sheet side by side (on grey) for eye review of a unit's one-sheet drawing.

  py -3.11 -X utf8 scripts/verify/sheet_side_by_side.py <unit number> [max width]
writes <set>/SHEET_REVIEW.png
"""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image


def main():
    u=int(sys.argv[1]);mw=int(sys.argv[2]) if len(sys.argv)>2 else 1800
    rs=ROOT/f'test_current/parts/pose_packets/unit_{u}/robot_set'
    if (rs/'COMBINED/candidate_combined.png').exists() and u==2:nat,can=rs/'COMBINED/native_combined_4x.png',rs/'COMBINED/candidate_combined.png'
    else:
        sh=rs/'unified_sheet';can=sh/'candidate_sheet.png'
        nat=next((p for p in sorted(sh.glob('native*.png')) if 'preview' not in p.name),None)
    a=Image.open(nat).convert('RGBA');b=Image.open(can).convert('RGBA').resize(a.size)
    W,H=a.size;out=Image.new('RGBA',(W*2+24,H),(80,82,92,255))
    for k,im in enumerate((a,b)):
        bg=Image.new('RGBA',im.size,(80,82,92,255));bg.alpha_composite(im);out.paste(bg,(k*(W+24),0))
    out.thumbnail((mw,mw));out.save(rs/'SHEET_REVIEW.png');print(rs/'SHEET_REVIEW.png',out.size)


if __name__=='__main__':main()
