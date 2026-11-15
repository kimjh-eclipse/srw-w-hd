"""Are a unit's palette variants (fades, flashes) a fixed blend of the main palette?

For every shape (index hash) of a robot set, compares each variant palette with
the main palette over the colour slots the shape uses. Fits, per variant, the
game-style blend  v = m*(1-t) + c*t  (one t, one target colour c) by least
squares and reports the worst slot error in 5-bit units. A variant that fits
within 1 step can be made from the main HD drawing by the same blend, with no
per-pixel slot guessing.

  py -3.11 -X utf8 scripts/verify/palette_variant_fit.py <set dir>
"""
import base64,json,sys,zlib
from collections import defaultdict
from pathlib import Path
import numpy as np


def rgb5(p):
    p=np.asarray(p,dtype='int64');return np.stack([p&31,(p>>5)&31,(p>>10)&31],-1).astype('float64')


def fit(m,v):
    """Least squares for v = m*(1-t)+c*t over t in [0,1] (grid) and c (closed form)."""
    best=None
    for t in np.linspace(0,1,101):
        if t==0:c=np.zeros(3);err=np.abs(v-m).max()
        else:
            c=((v-m*(1-t))/t).mean(0).clip(0,31);err=np.abs(m*(1-t)+c*t-v).max()
        if best is None or err<best[0]:best=(float(err),float(t),c.round(1).tolist())
    return best


def main():
    root=Path(sys.argv[1]);shapes=json.loads((root/'SHAPES.json').read_text(encoding='utf-8'))
    rows={}
    unit=root.parent
    for c in unit.glob('weapon_*/objects/obj_*/contract.json'):
        for r in json.loads(c.read_text(encoding='utf-8')):rows.setdefault(r['hash'],r)
    stats=defaultdict(int);out=[]
    for ih,main_hash in shapes['main_palette'].items():
        m=rows.get(main_hash)
        if m is None:continue
        idx=np.frombuffer(zlib.decompress(base64.b64decode(m['index_pixels'])),dtype='uint8');used=sorted(set(idx[idx>0].tolist()))
        M=rgb5(m['palette_15bit'])[used]
        for h in shapes['variants'][ih]:
            if h==main_hash or h not in rows:continue
            V=rgb5(rows[h]['palette_15bit'])[used];err,t,c=fit(M,V)
            # Per-channel linear map v = a*m + b (channel-specific fade rates).
            perr=0.;coef=[]
            for ch in range(3):
                A=np.stack([M[:,ch],np.ones(len(M))],1);sol,*_=np.linalg.lstsq(A,V[:,ch],rcond=None)
                perr=max(perr,float(np.abs(A@sol-V[:,ch]).max()));coef.append([round(float(sol[0]),3),round(float(sol[1]),2)])
            # Same, clamped at 0 and 31 (fades that bottom out): fit on unclamped slots.
            cerr=0.
            for ch in range(3):
                keep=(V[:,ch]>0)&(V[:,ch]<31)
                if keep.sum()>=2:
                    A=np.stack([M[keep,ch],np.ones(int(keep.sum()))],1);sol,*_=np.linalg.lstsq(A,V[keep,ch],rcond=None)
                else:sol=np.array([0.,float(V[:,ch].mean())])
                pred=np.clip(M[:,ch]*sol[0]+sol[1],0,31);cerr=max(cerr,float(np.abs(np.round(pred)-V[:,ch]).max()))
            kind='blend' if err<=1.01 else 'channel_linear' if perr<=1.01 else 'clamped_linear' if cerr<=1.01 else 'other';stats[kind]+=1
            out.append(dict(shape=int(ih),variant=h,slots=len(used),max_err=round(err,2),t=round(t,2),target=c,channel_err=round(perr,2),channel_map=coef,kind=kind))
    (root/'VARIANT_FIT.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
    print(dict(stats),'of',len(out))
    others=[o for o in out if o['kind']=='other']
    for o in others[:8]:print(o)
    ts=sorted({(round(o['t'],1),tuple(round(x) for x in o['target'])) for o in out if o['kind']=='blend'})
    print('blend kinds',len(ts),ts[:20])


if __name__=='__main__':main()
