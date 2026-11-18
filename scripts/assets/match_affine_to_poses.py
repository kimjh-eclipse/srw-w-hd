"""Find, for each affine pose (pose_aNN), a normal pose of the same unit that shows the same picture.

An affine object is often the unit's ordinary pose drawn into one texture and
then scaled/rotated by the game. Then no new drawing is needed: the HD of that
normal pose (pose_NN/candidate_fit.png, 4x) is cut at the same place.

Matching: the affine native picture (opaque pixels and colours) is searched in
each normal pose's native.png (also mirrored) at the offset that aligns the
opaque bounding boxes, then +-3 px around it. A match needs >= 97% of the
affine opaque pixels with the same colour.

  py -3.11 -X utf8 scripts/assets/match_affine_to_poses.py <unit> [...]   -> robot_set/AFFINE_MATCH.json
"""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

BASE=ROOT/'test_current/parts/pose_packets'


def load(p):
    a=np.asarray(Image.open(p).convert('RGBA'));return a[:,:,:3].astype(int),a[:,:,3]>0


def bbox(m):
    ys,xs=np.where(m);return (xs.min(),ys.min(),xs.max()+1,ys.max()+1) if len(xs) else None


def best_match(arg,am,nrg,nm):
    ab=bbox(am);nb=bbox(nm)
    if ab is None or nb is None:return 0,None
    H,W=nm.shape;h,w=am.shape;best=(0,None)
    for ox0 in range(-3,4):
        for oy0 in range(-3,4):
            ox=nb[0]-ab[0]+ox0;oy=nb[1]-ab[1]+oy0   # affine pixel (x,y) -> normal (x+ox,y+oy)
            ys,xs=np.where(am);tx,ty=xs+ox,ys+oy
            ok=(tx>=0)&(ty>=0)&(tx<W)&(ty<H)
            if ok.mean()<.97:continue
            same=np.zeros(len(xs),bool)
            same[ok]=nm[ty[ok],tx[ok]]&(np.abs(nrg[ty[ok],tx[ok]]-arg[ys[ok],xs[ok]]).sum(1)<=24)
            s=same.mean()
            if s>best[0]:best=(s,(int(ox),int(oy)))
    return best


def match_unit(u):
    rs=BASE/f'unit_{u}/robot_set';out={}
    normals=sorted(d for d in rs.glob('pose_[0-9]*') if (d/'native.png').exists())
    cache={d.name:load(d/'native.png') for d in normals}
    for ap in sorted(rs.glob('pose_a*')):
        arg,am=load(ap/'native.png');res=dict(match=None)
        for name,(nrg,nm) in cache.items():
            for mirror in (False,True):
                a_rgb,a_m=(arg[:,::-1],am[:,::-1]) if mirror else (arg,am)
                s,off=best_match(a_rgb,a_m,nrg,nm)
                if s>=.97 and (res['match'] is None or s>res['score']):
                    res=dict(match=name,score=round(float(s),4),offset=off,mirror=mirror)
        out[ap.name]=res
    (rs/'AFFINE_MATCH.json').write_text(json.dumps(out,indent=1),encoding='utf-8')
    return out


if __name__=='__main__':
    for u in map(int,sys.argv[1:]):
        r=match_unit(u);print(u,{k:(v['match'],v.get('score')) for k,v in r.items()},flush=True)
