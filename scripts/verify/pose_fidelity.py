"""How faithful is each installed pose drawing to its native sprite? (re-review 11/21, Gates lesson)

Per accepted pose: the fitted drawing (candidate_fit.png, 4x) is reduced to native size (box) and
compared with native.png where the native sprite is opaque:
  sil_iou     silhouette IoU (drawing alpha vs native alpha)         -> wrong outline / positions
  mean_diff   mean RGB difference over the native silhouette          -> wrong colouring overall
  worst_block worst mean RGB difference in any 6x6 native block      -> one wrong region (a white
              that covers >= 60% opaque native pixels                   jaw on a dark face, a moved arm)
  shift       best whole-pixel offset (-2..2) of the drawing vs native (0,0 = aligned)
Writes test_current/parts/pose_packets/POSE_FIDELITY.json.

  py -3.11 -X utf8 scripts/verify/pose_fidelity.py [--units 74,11]
"""
import argparse,json,sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets'


def pose(folder):
    try:
        nat=np.asarray(Image.open(folder/'native.png').convert('RGBA')).astype(int);H,W=nat.shape[:2]
        d=Image.open(folder/'candidate_fit.png').convert('RGBA')
        if d.size!=(W*4,H*4):return None
        small=np.asarray(d.resize((W,H),Image.Resampling.BOX)).astype(int)
    except Exception:return None
    m=nat[...,3]>0;dm=small[...,3]>128
    if m.sum()<20:return None
    iou=float((m&dm).sum()/max(1,(m|dm).sum()))
    best=(1e9,0,0)
    for dy in range(-2,3):
        for dx in range(-2,3):
            s=np.roll(np.roll(small,dy,0),dx,1);mm=m&(s[...,3]>128)
            if mm.sum()<10:continue
            v=float(np.abs(s[...,:3]-nat[...,:3])[mm].mean())
            if v<best[0]:best=(v,dy,dx)
    both=m&dm;diff=np.abs(small[...,:3]-nat[...,:3]).mean(2)
    mean=float(diff[both].mean()) if both.any() else 255.
    worst=0.;wb=None
    for y in range(0,H-5,3):
        for x in range(0,W-5,3):
            blk=m[y:y+6,x:x+6]
            if blk.sum()<22:continue
            sel=both[y:y+6,x:x+6]
            v=float(diff[y:y+6,x:x+6][sel].mean()) if sel.sum()>=10 else 255.
            if v>worst:worst,wb=v,(x,y)
    return dict(sil_iou=round(iou,3),mean_diff=round(mean,1),worst_block=round(worst,1),worst_at=wb,shift=[best[1],best[2]])


def unit(rs):
    st=rs/'DRAWINGS_STATUS.json'
    if not st.exists():return rs.parent.name,{}
    acc=[k for k,v in json.loads(st.read_text(encoding='utf-8')).items() if v.get('state')=='accepted']
    out={}
    for k in acc:
        r=pose(rs/k)
        if r:out[k]=r
    return rs.parent.name,out


def main():
    p=argparse.ArgumentParser();p.add_argument('--units',default='');a=p.parse_args()
    sets=[rs for rs in sorted(BASE.glob('unit_*/robot_set')) if (rs/'INSTALLED').exists() or (rs/'HOLD_REDRAW').exists()]
    if a.units:sets=[BASE/f'unit_{u}/robot_set' for u in a.units.split(',')]
    res={}
    with ProcessPoolExecutor(6) as ex:
        for u,r in ex.map(unit,sets):res[u]=r
    out=BASE/('POSE_FIDELITY.json' if not a.units else 'POSE_FIDELITY_sample.json')
    out.write_text(json.dumps(res,indent=0),encoding='utf-8');print('units',len(res),'poses',sum(len(v) for v in res.values()),out)


if __name__=='__main__':main()
