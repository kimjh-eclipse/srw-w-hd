"""HD version of a unit's ORIGINAL part sheet, cut from Codex pose drawings part by part (user 11/21).

The ROM stores each robot as one part sheet (IMG, e.g. 256x32); every OAM sprite is a crop of it
at (u, v). A part = one connected drawn area of the sheet. For each part, the pose drawing where
that part is most visible is used, and the part is cut out of that one drawing in the part's own
shape and size (its sheet silhouette, enlarged smoothly), then placed at its sheet position (4x).
Every sprite then crops this HD sheet like the game crops the original, so all poses share the
same part picture and no sprite edge is cut on its own.

Output: <robot_set>/split_sheet/parts/<hash>.png (texture orientation) + cov/ + coverage.json,
HD_SHEET.png and SHEET_SOURCES.json. Then package_robot_set.py <set> --split split_sheet.

  py -3.11 -X utf8 scripts/assets/sheet_parts_from_poses.py 196
"""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageFilter
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from scripts.assets.build_object_packets import compose_canvas
BASE=ROOT/'test_current/parts/pose_packets';S=4


def comps8(mask):
    H,W=mask.shape;lab=np.where(mask,np.arange(1,H*W+1).reshape(H,W),0);big=H*W+2
    while True:
        cur=np.where(mask,lab,big);m=cur.copy()
        for dy in (-1,0,1):
            for dx in (-1,0,1):
                if dy==0 and dx==0:continue
                sh=np.full_like(cur,big);sh[max(dy,0):H+min(dy,0),max(dx,0):W+min(dx,0)]=cur[max(-dy,0):H+min(-dy,0),max(-dx,0):W+min(-dx,0)]
                m=np.minimum(m,sh)
        m=np.where(mask,m,0)
        if np.array_equal(m,lab):return lab
        lab=m


def main():
    uid=int(sys.argv[1]);rs=BASE/f'unit_{uid}/robot_set'
    cat=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    res=next(u for u in cat['units'] if u['unit_id']==uid)['primary_image']
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();off=g.archive(rom)
    sheet=g.pixels(g.decompress(rom[g.BASE+off[res]:g.BASE+off[res+1]]));SH,SW=sheet.shape
    accepted=json.loads((rs/'accepted_poses.json').read_text()) if (rs/'accepted_poses.json').exists() else [k for k,v in json.loads((rs/'DRAWINGS_STATUS.json').read_text(encoding='utf-8')).items() if v.get('state')=='accepted']
    # where each sprite comes from in the sheet: exact index match (with flips)
    where={}
    def locate(r):
        h=r['hash']
        if h in where:return where[h]
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(r['h'],r['w'])
        for v in range(0,SH-r['h']+1):
            for u in range(0,SW-r['w']+1):
                c=sheet[v:v+r['h'],u:u+r['w']]
                if np.array_equal(c,idx):where[h]=(u,v);return where[h]
        where[h]=None;return None
    poses={}
    for p in accepted:
        f=rs/p
        if not ((f/'contract.json').exists() and (f/'candidate_fit.png').exists()):continue
        rows=json.loads((f/'contract.json').read_text(encoding='utf-8'));W,H=Image.open(f/'native.png').size
        _,label=compose_canvas(rows,W,H);poses[p]=(rows,label,np.asarray(Image.open(f/'candidate_fit.png').convert('RGBA')))
        for r in rows:locate(r)
    comp=comps8(sheet>0);ids=[i for i in np.unique(comp) if i]
    hd=np.zeros((SH*S,SW*S,4),dtype='uint8');cov=np.zeros((SH*S,SW*S),dtype=bool);src={}
    for cid in ids:
        part=comp==cid;best=None
        for p,(rows,label,art) in poses.items():
            # every sheet texel of this part -> (screen x, y) through the sprite that shows it, if visible
            vis=0;tot=int(part.sum());maps=[]
            for k,r in enumerate(rows):
                loc=where.get(r['hash'])
                if loc is None:continue
                u,v=loc;sub=part[v:v+r['h'],u:u+r['w']]
                if not sub.any():continue
                yy,xx=np.nonzero(sub)
                sx=(r['w']-1-xx) if r['flip_x'] else xx;sy=(r['h']-1-yy) if r['flip_y'] else yy
                X=r['screen_x']+sx;Y=r['screen_y']+sy;ok=(X>=0)&(Y>=0)&(X<label.shape[1])&(Y<label.shape[0])
                front=np.zeros_like(ok);front[ok]=label[Y[ok],X[ok]]==k
                vis+=int(front.sum());maps.append((k,r,u,v))
            if not maps:continue
            score=vis/tot
            if best is None or score>best[0]:best=(score,p,maps)
        if best is None:continue
        score,p,maps=best;rows,label,art=poses[p];src[int(cid)]=dict(pose=p,visible=round(score,3))
        # smooth part silhouette at 4x (the part's own outline, interpolated)
        ys,xs=np.nonzero(part);y0,y1,x0,x1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
        pm=Image.fromarray((part[y0:y1,x0:x1]*255).astype('uint8')).resize(((x1-x0)*S,(y1-y0)*S),Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(3))
        pm=np.asarray(pm)>=128
        for k,r,u,v in maps:
            # 4x texels of this sprite's crop that belong to the part (smooth mask), sampled from the pose drawing
            for ty in range(r['h']*S):
                gy=v*S+ty
                if gy<y0*S or gy>=y1*S:continue
                row=pm[gy-y0*S]
                for tx in range(r['w']*S):
                    gx=u*S+tx
                    if gx<x0*S or gx>=x1*S or not row[gx-x0*S] or cov[gy,gx]:continue
                    sx=(r['w']*S-1-tx) if r['flip_x'] else tx;sy=(r['h']*S-1-ty) if r['flip_y'] else ty
                    X=r['screen_x']*S+sx;Y=r['screen_y']*S+sy
                    if 0<=X<art.shape[1] and 0<=Y<art.shape[0] and art[Y,X,3]>0:hd[gy,gx]=art[Y,X];cov[gy,gx]=True
    out=rs/'split_sheet';(out/'parts').mkdir(parents=True,exist_ok=True);(out/'cov').mkdir(exist_ok=True)
    Image.fromarray(hd).save(rs/'HD_SHEET.png')
    report=[]
    for h,loc in where.items():
        if loc is None:continue
        u,v=loc;r=next(r for p in poses.values() for r in p[0] if r['hash']==h)
        crop=hd[v*S:(v+r['h'])*S,u*S:(u+r['w'])*S];c=cov[v*S:(v+r['h'])*S,u*S:(u+r['w'])*S]
        Image.fromarray(crop).save(out/'parts'/f'{h}.png');Image.fromarray((c*255).astype('uint8')).save(out/'cov'/f'{h}.png')
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(r['h'],r['w'])
        need=np.kron(idx>0,np.ones((S,S),bool));report.append(dict(hash=h,binding_id=r['binding_id'],w=r['w'],h=r['h'],coverage=round(float((c&need).sum()/max(need.sum(),1)),3)))
    (out/'coverage.json').write_text(json.dumps(report,indent=1),encoding='utf-8')
    (rs/'SHEET_SOURCES.json').write_text(json.dumps(dict(resource=res,parts=src,unlocated=[h for h,l in where.items() if l is None]),indent=1),encoding='utf-8')
    print('unit',uid,'sheet',res,(SW,SH),'parts',len(ids),'drawn',len(src),'sprites located',sum(1 for l in where.values() if l),'/',len(where))


if __name__=='__main__':main()
