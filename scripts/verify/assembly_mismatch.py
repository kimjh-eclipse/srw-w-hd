"""Do a unit's installed parts still form each pose's own drawing? (11/21)

Each accepted pose is assembled from the unit's split parts (split_fit/parts, back to front, flips)
like the game does, and compared with that pose's drawing (candidate_fit.png) inside the native
silhouette. Parts drawn the same way in every pose -> small difference (only cut edges). Parts
drawn at another size/place in another pose -> large difference (seams, wrong head). Per pose:
share of silhouette pixels whose colour differs by > 60, measured at native size (box), so the
cut edge itself (smoothing) is not counted. Writes ASSEMBLY_MISMATCH.json.

  py -3.11 -X utf8 scripts/verify/assembly_mismatch.py [--units 196,11]
"""
import argparse,json,sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets'


def unit(rs):
    st=rs/'DRAWINGS_STATUS.json';parts=rs/'split_fit/parts'
    if not st.exists() or not parts.exists():return rs.parent.name,None
    acc=[k for k,v in json.loads(st.read_text(encoding='utf-8')).items() if v.get('state')=='accepted'];res={}
    cache={}
    for p in acc:
        f=rs/p
        if not ((f/'contract.json').exists() and (f/'candidate_fit.png').exists()):continue
        rows=json.loads((f/'contract.json').read_text(encoding='utf-8'));nat=Image.open(f/'native.png').convert('RGBA');W,H=nat.size
        can=Image.new('RGBA',(W*4,H*4))
        for r in reversed(rows):
            q=parts/f"{r['hash']}.png"
            if not q.exists():continue
            if q not in cache:cache[q]=Image.open(q).convert('RGBA')
            im=cache[q]
            if r['flip_x']:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if r['flip_y']:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            can.alpha_composite(im,(r['screen_x']*4,r['screen_y']*4))
        a=np.asarray(can.resize((W,H),Image.Resampling.BOX)).astype(int)
        b=np.asarray(Image.open(f/'candidate_fit.png').convert('RGBA').resize((W,H),Image.Resampling.BOX)).astype(int)
        m=(np.asarray(nat)[...,3]>0)&(a[...,3]>200)&(b[...,3]>200)
        if m.sum()<50:continue
        d=np.abs(a[...,:3]-b[...,:3]).max(2)
        res[p]=round(float((d[m]>60).mean()),3)
    return rs.parent.name,res


def main():
    a=argparse.ArgumentParser();a.add_argument('--units',default='');a=a.parse_args()
    sets=[BASE/f'unit_{u}/robot_set' for u in a.units.split(',')] if a.units else [rs for rs in sorted(BASE.glob('unit_*/robot_set')) if (rs/'INSTALLED').exists() or (rs/'HOLD_REDRAW').exists()]
    out={}
    with ProcessPoolExecutor(8) as ex:
        for u,r in ex.map(unit,sets):
            if r:out[u]=dict(mean=round(float(np.mean(list(r.values()))),3),worst=max(r.values()),poses=r)
    (BASE/('ASSEMBLY_MISMATCH.json' if not a.units else 'ASSEMBLY_MISMATCH_sample.json')).write_text(json.dumps(out,indent=0),encoding='utf-8')
    for u,v in sorted(out.items(),key=lambda kv:-kv[1]['mean'])[:12]:print(u,v['mean'],v['worst'])
    print('units',len(out))


if __name__=='__main__':main()
