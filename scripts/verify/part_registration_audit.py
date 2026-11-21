"""Which units' drawings put the original parts at a different size/position? (11/21)

For every accepted pose and every sprite of >= 16x16 that is mostly in front (>= 60% visible):
the drawing (2x, blurred) is searched for the part around its native place over scales 0.8-1.25
and offsets +-6 native px; the best match gives (scale, dx, dy) in native px. A part is OFF when
|scale-1| > 0.06 or the offset is > 1 native px. Writes PART_REGISTRATION.json.

  py -3.11 -X utf8 scripts/verify/part_registration_audit.py [--units 196,60] [--procs 8]
"""
import argparse,base64,json,sys,zlib
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets';Z=2


def audit_pose(folder):
    from scripts.assets.build_object_packets import compose_canvas
    rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'));nat=Image.open(folder/'native.png').convert('RGBA');W,H=nat.size
    _,label=compose_canvas(rows,W,H)
    ref=nat.resize((W*Z,H*Z),Image.Resampling.NEAREST).filter(ImageFilter.GaussianBlur(1.2))
    src=Image.open(folder/'candidate_fit.png').convert('RGBA').resize((W*Z,H*Z),Image.Resampling.BOX).filter(ImageFilter.GaussianBlur(1.2))
    refa=np.asarray(ref,dtype=np.float32);out=[]
    for k,r in enumerate(rows):
        w,h=r['w'],r['h']
        if w*h<256:continue
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(h,w)>0
        if r['flip_y']:idx=idx[::-1]
        if r['flip_x']:idx=idx[:,::-1]
        x,y=r['screen_x'],r['screen_y'];reg=label[max(0,y):y+h,max(0,x):x+w]
        if reg.size==0:continue
        sub=idx[:reg.shape[0],:reg.shape[1]];vis=float((reg==k)[sub].mean()) if sub.any() else 0
        if vis<0.6:continue
        sel=np.kron((label==k).astype(bool),np.ones((Z,Z),bool))[y*Z:(y+h)*Z,x*Z:(x+w)*Z] if x>=0 and y>=0 else None
        if sel is None or sel.sum()<64:continue
        X0,Y0,PW,PH=x*Z,y*Z,w*Z,h*Z;cx,cy=X0+PW/2,Y0+PH/2;R=refa[Y0:Y0+PH,X0:X0+PW,:3]
        if R.shape[:2]!=sel.shape:continue
        def score(s,dx,dy):
            bw,bh=PW*s,PH*s;l=cx-bw/2+dx;t=cy-bh/2+dy
            a=np.asarray(src.transform((PW,PH),Image.Transform.EXTENT,(l,t,l+bw,t+bh),Image.Resampling.BILINEAR),dtype=np.float32)
            m=sel&(a[...,3]>100)
            if m.sum()<0.6*sel.sum():return 1e9
            return float(np.abs(a[...,:3]-R)[m].mean())
        best=(score(1,0,0),1.0,0,0)
        for s in (0.8,0.85,0.9,0.95,1.0,1.05,1.1,1.15,1.2,1.25):
            for dy in range(-12,13,3):
                for dx in range(-12,13,3):
                    v=score(s,dx,dy)
                    if v<best[0]:best=(v,s,dx,dy)
        v0=score(1,0,0)
        _,s,dx,dy=best
        out.append(dict(hash=r['hash'],w=w,h=h,scale=s,dx=dx/Z,dy=dy/Z,gain=round(v0-best[0],1),off=bool(abs(s-1)>0.06 or max(abs(dx),abs(dy))/Z>1.0) and v0-best[0]>3))
    return out


def unit(rs):
    st=rs/'DRAWINGS_STATUS.json'
    if not st.exists():return rs.parent.name,None
    acc=[k for k,v in json.loads(st.read_text(encoding='utf-8')).items() if v.get('state')=='accepted']
    res={}
    for p in acc:
        f=rs/p
        if (f/'candidate_fit.png').exists() and (f/'contract.json').exists():
            try:res[p]=audit_pose(f)
            except Exception as e:res[p]=dict(error=str(e)[:100])
    return rs.parent.name,res


def main():
    a=argparse.ArgumentParser();a.add_argument('--units',default='');a.add_argument('--procs',type=int,default=8);a=a.parse_args()
    sets=[BASE/f'unit_{u}/robot_set' for u in a.units.split(',')] if a.units else [rs for rs in sorted(BASE.glob('unit_*/robot_set')) if (rs/'INSTALLED').exists() or (rs/'HOLD_REDRAW').exists()]
    out={}
    with ProcessPoolExecutor(a.procs) as ex:
        for n,(u,r) in enumerate(ex.map(unit,sets),1):
            if r is None:continue
            parts=[x for v in r.values() if isinstance(v,list) for x in v];off=[x for x in parts if x['off']]
            out[u]=dict(parts=len(parts),off=len(off),share=round(len(off)/max(1,len(parts)),3),poses_with_off=sorted(p for p,v in r.items() if isinstance(v,list) and any(x['off'] for x in v)),detail=r)
            if n%25==0:print('units',n,'/',len(sets),flush=True)
    name='PART_REGISTRATION.json' if not a.units else 'PART_REGISTRATION_sample.json'
    (BASE/name).write_text(json.dumps(out,indent=0),encoding='utf-8')
    for u,v in sorted(out.items(),key=lambda kv:-kv[1]['share'])[:15]:print(u,v['parts'],v['off'],v['share'])


if __name__=='__main__':main()
