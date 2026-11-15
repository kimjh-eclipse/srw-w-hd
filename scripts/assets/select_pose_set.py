"""Pick the fewest poses whose drawings give every sprite its pixels.

A sprite's pixel can be cut from a pose drawing only where that sprite is in
front. Across poses the same sprite (same hash) may be visible in different
places, so its HD can be stitched from several poses. This greedily picks
poses that add the most not-yet-covered sprite pixels, until coverage stops
growing, and reports what stays hidden in every pose (those pixels can never
come from a pose drawing and need a separate whole-part drawing).

  py -3.11 -X utf8 scripts/assets/select_pose_set.py <pose packet dir>
"""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.assets.build_pose_packets import compose,sprite_pixels


def main():
    root=Path(sys.argv[1]);poses=sorted(d for d in root.glob('pose_*') if d.is_dir())
    need={};gain={}
    for p in poses:
        rows=json.loads((p/'contract.json').read_text(encoding='utf-8'))
        _,label=compose(rows);g={}
        for k,r in enumerate(rows):
            idx=sprite_pixels(r);opaque=idx>0;h=r['hash']
            vis=np.zeros_like(opaque)
            x,y,w,hh=r['screen_x'],r['screen_y'],r['w'],r['h']
            for yy in range(hh):
                sy=y+yy
                if not 0<=sy<192:continue
                for xx in range(w):
                    sx=x+xx
                    if 0<=sx<256 and label[sy,sx]==k:vis[yy,xx]=True
            # back to texture orientation
            if r['flip_y']:vis=vis[::-1];opaque=opaque[::-1]
            if r['flip_x']:vis=vis[:,::-1];opaque=opaque[:,::-1]
            need.setdefault(h,opaque.copy())
            g[h]=g.get(h,np.zeros_like(opaque))|vis
        gain[p.name]=g
    covered={h:np.zeros_like(m) for h,m in need.items()};chosen=[]
    total=sum(int(m.sum()) for m in need.values())
    while True:
        best=None
        for name,g in gain.items():
            if name in chosen:continue
            add=sum(int((v&~covered[h]&need[h]).sum()) for h,v in g.items())
            if best is None or add>best[1]:best=(name,add)
        if not best or best[1]<=0:break
        chosen.append(best[0])
        for h,v in gain[best[0]].items():covered[h]|=v&need[h]
    got=sum(int(covered[h].sum()) for h in need)
    per=[(h,int(need[h].sum()),int(covered[h].sum())) for h in need]
    weak=[x for x in per if x[2]<x[1]*.9]
    out=dict(poses_total=len(poses),poses_chosen=len(chosen),chosen=chosen,sprites=len(need),pixels=total,covered=got,
        coverage=round(got/max(total,1),4),sprites_under_90pct=len(weak),never_visible_pixels=total-got,
        weak_sprites=sorted([dict(hash=h,opaque=o,covered=c) for h,o,c in weak],key=lambda d:d['covered']/max(d['opaque'],1))[:40])
    (root/'POSE_SET.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
    print({k:v for k,v in out.items() if k not in ('chosen','weak_sprites')})
    print('first chosen',chosen[:20])


if __name__=='__main__':main()
