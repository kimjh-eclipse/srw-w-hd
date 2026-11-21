"""Cut drawn whole-object pictures back into per-sprite HD parts.

For every object folder (build_object_packets.py) that has a drawing
(candidate.png, 4x of native.png), each sprite takes the drawing's pixels
where that sprite is the one in front, un-flipped to texture orientation.
The same sprite (same hash) seen in several objects is merged; where two
objects give a pixel, the one where the sprite is less hidden wins.

Output per sprite: <out>/parts/<hash>.png (RGBA, 4x of the sprite size) plus
coverage.json (share of the sprite's opaque pixels that got drawing pixels).
Pixels no drawing gives are left transparent and reported - they were hidden in
every captured frame. Nothing is recoloured from another palette.

  --selftest  uses native_4x.png as the drawing and checks that re-assembling the
              cut parts reproduces every object exactly where it is visible.

  py -3.11 -X utf8 scripts/assets/split_object_drawings.py <objects dir> [--only list.json] [--selftest]
"""
import argparse,json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts.assets.build_pose_packets import sprite_pixels
from scripts.assets.build_object_packets import compose_canvas

S=4
# Outline ring (4x pixels): the drawing's own soft outline just outside the native
# silhouette goes to the nearest sprite, with the drawing's alpha. Without it the part's
# edge is the native pixel grid x4 (stair edges, user report 11/18-20). 0 = old behaviour.
EDGE_RING=int(__import__('os').environ.get('SRWW_EDGE_RING','4'))


def grow_labels(big,R):
    """Give exterior pixels (-1) within R steps the label of a neighbouring sprite pixel."""
    lab=big.copy();H,W=lab.shape
    for _ in range(R):
        empty=lab<0
        if not empty.any():break
        new=lab.copy()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)):
            sh=np.full_like(lab,-1)
            sh[max(-dy,0):H+min(-dy,0),max(-dx,0):W+min(-dx,0)]=lab[max(dy,0):H+min(dy,0),max(dx,0):W+min(dx,0)]
            fill=empty&(new<0)&(sh>=0);new[fill]=sh[fill]
        lab=new
    return lab


INK_SPLIT=__import__('os').environ.get('SRWW_INK_SPLIT','0')=='1'


def _components(mask):
    """4-connected component ids (0 = background) by min-label propagation."""
    H,W=mask.shape;lab=np.where(mask,np.arange(1,H*W+1).reshape(H,W),0)
    big=H*W+2
    while True:
        cur=np.where(mask,lab,big);m=cur.copy()
        m[1:]=np.minimum(m[1:],cur[:-1]);m[:-1]=np.minimum(m[:-1],cur[1:]);m[:,1:]=np.minimum(m[:,1:],cur[:,:-1]);m[:,:-1]=np.minimum(m[:,:-1],cur[:,1:])
        m=np.where(mask,m,0)
        if np.array_equal(m,lab):return lab
        lab=m


def ink_labels(art,base,ring):
    """Split along the DRAWN lines, not the native pixel grid (user 11/21): every region of the
    drawing enclosed by its dark ink lines goes whole to the sprite that owns most of it natively;
    ink and soft rim pixels take the label of the nearest region. Regions without a clear owner
    (<60% one sprite) keep the native per-pixel labels. Nothing is drawn past the drawing's alpha."""
    a=art[...,3];ink=(a>128)&(art[...,:3].max(2)<80);fill=(a>128)&~ink
    comp=_components(fill);lab=np.full(base.shape,-1,dtype=base.dtype)
    ids,inv=np.unique(comp[fill],return_inverse=True);owner=base[fill]
    n=int(base.max())+2
    counts=np.zeros((len(ids),n),dtype=np.int64);np.add.at(counts,(inv,owner+1),1)
    best=counts[:,1:].argmax(1);share=counts[:,1:].max(1)/np.maximum(counts.sum(1),1)
    choice=np.where(share>=0.6,best,-2)[inv]
    vals=np.where(choice>=0,choice,owner);lab[fill]=vals
    lab[fill&(lab<0)&(base>=0)]=base[fill&(lab<0)&(base>=0)]
    # ink and rim: nearest labelled pixel within the drawing, a few steps
    rest=(a>0)&(lab<0)
    for _ in range(12):
        if not rest.any():break
        H,W=lab.shape;new=lab.copy()
        for dy,dx in ((-1,0),(1,0),(0,-1),(0,1)):
            sh=np.full_like(lab,-1);sh[max(-dy,0):H+min(-dy,0),max(-dx,0):W+min(-dx,0)]=lab[max(dy,0):H+min(dy,0),max(dx,0):W+min(dx,0)]
            f=rest&(new<0)&(sh>=0);new[f]=sh[f]
        lab=new;rest=(a>0)&(lab<0)
    return np.where(ring>=0,lab,-1) if ring is not None else lab


FULL_PART=__import__('os').environ.get('SRWW_FULL_PART','0')=='1'
SMOOTH_CUT=__import__('os').environ.get('SRWW_SMOOTH_CUT','1')=='1'


def smooth_labels(label):
    """Native ownership map -> 4x map whose borders are interpolated, not the pixel staircase
    (user 11/21: 'cut diagonals as diagonals, interpolate like a filter'). Each label's one-hot
    plane is enlarged bilinearly and blurred a little; every 4x pixel takes the strongest label.
    Background (-1) is a label too, so the outer silhouette is smoothed the same way."""
    from PIL import Image,ImageFilter
    H,W=label.shape;ids=np.unique(label);best=None;arg=None
    for v in ids:
        plane=Image.fromarray(((label==v)*255).astype('uint8')).resize((W*S,H*S),Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(float(__import__('os').environ.get('SRWW_CUT_BLUR','4'))))
        a=np.asarray(plane,dtype=np.int16)
        if best is None:best=a.copy();arg=np.full(a.shape,v,dtype=label.dtype)
        else:
            m=a>best;best[m]=a[m];arg[m]=v
    return arg


def _dilate(m,n):
    for _ in range(n):
        g=m.copy();g[1:]|=m[:-1];g[:-1]|=m[1:];g[:,1:]|=m[:,:-1];g[:,:-1]|=m[:,1:];m=g
    return m


def line_cut_masks(art,big,rows):
    """Cut along the drawn lines (user 11/21). Painted areas between the dark ink lines are
    regions; inside a sprite's rectangle a region goes to the sprite when the sprite natively
    owns at least half of that region's pixels there. Specks (<48 px) follow the region next to
    them. The ink line around the taken regions goes with them, and the soft rim outside the
    ink. Neighbouring pieces may share an ink line (identical pixels). No native-grid edge."""
    a=art[...,3];ink=(a>96)&(art[...,:3].max(2)<85);fill=(a>96)&~ink
    comp=_components(fill);near=_dilate(big>=0,10)
    sizes=np.bincount(comp.ravel())
    out={}
    for k,r in enumerate(rows):
        x,y,w,h=r['screen_x']*S,r['screen_y']*S,r['w']*S,r['h']*S
        c=comp[y:y+h,x:x+w];own=big[y:y+h,x:x+w]==k;f=fill[y:y+h,x:x+w]
        ids=np.unique(c[f]);take=np.zeros_like(own)
        if len(ids):
            tot=np.bincount(c[f],minlength=int(c.max())+1);mine_n=np.bincount(c[f&own],minlength=int(c.max())+1)
            good=[i for i in ids if sizes[i]>=48 and mine_n[i]>=0.5*tot[i]]
            take=np.isin(c,good)&f
            small=f&np.isin(c,[i for i in ids if sizes[i]<48])
            take|=small&_dilate(take,3)
        take&=near[y:y+h,x:x+w]
        line=ink[y:y+h,x:x+w]&_dilate(take,4)
        rim=(a[y:y+h,x:x+w]>0)&~fill[y:y+h,x:x+w]&~ink[y:y+h,x:x+w]&_dilate(take|line,2)
        out[k]=take|line|rim
    return out


def register_piece(art,native4,x,y,w,h,op):
    """Locate one original part inside the HD drawing: try scales and offsets around the part's
    native place, compare the drawing (blurred) with the native 4x pixels over the part's own
    pixels, and return the drawing resampled so the found part fills the part's 4x box."""
    from PIL import Image as _I,ImageFilter as _F
    X0,Y0,PW,PH=x*S,y*S,w*S,h*S;cx,cy=X0+PW/2,Y0+PH/2
    sel=np.kron(op,np.ones((S,S),bool))
    ref=np.asarray(_I.fromarray(native4.astype('uint8')).crop((X0,Y0,X0+PW,Y0+PH)).filter(_F.GaussianBlur(3)),dtype=np.float32)
    src=_I.fromarray(art).filter(_F.GaussianBlur(3))
    def sample(img,s,dx,dy):
        # box of the part scaled by s about its centre, shifted by (dx, dy), resampled to PW x PH
        bw,bh=PW*s,PH*s;l=cx-bw/2+dx;t=cy-bh/2+dy
        return np.asarray(img.transform((PW,PH),_I.Transform.EXTENT,(l,t,l+bw,t+bh),_I.Resampling.BILINEAR),dtype=np.float32)
    def score(a):
        m=sel&(a[...,3]>100)
        if m.sum()<0.6*sel.sum():return 1e9
        return float(np.abs(a[...,:3]-ref[...,:3])[m].mean())+40*(1-m.sum()/max(1,sel.sum()))
    best=(score(sample(src,1.0,0,0)),1.0,0,0)
    for s in (0.8,0.85,0.9,0.95,1.0,1.05,1.1,1.15,1.2,1.25):
        for dy in range(-16,17,4):
            for dx in range(-16,17,4):
                v=score(sample(src,s,dx,dy))
                if v<best[0]:best=(v,s,dx,dy)
    _,s,dx,dy=best
    for ddy in (-2,-1,0,1,2):
        for ddx in (-2,-1,0,1,2):
            v=score(sample(src,s,dx+ddx,dy+ddy))
            if v<best[0]:best=(v,s,dx+ddx,dy+ddy)
    _,s,dx,dy=best
    return sample(_I.fromarray(art),s,dx,dy).clip(0,255).astype('uint8')


def cut(folder,drawing):
    rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'))
    native=Image.open(folder/'native.png');W,H=native.size
    _,label=compose_canvas(rows,W,H)
    art=np.asarray(drawing.convert('RGBA'))
    assert art.shape[:2]==(H*S,W*S),(folder.name,art.shape,(H*S,W*S))
    big=smooth_labels(label) if SMOOTH_CUT else np.repeat(np.repeat(label,S,0),S,1)
    line_masks=None
    native4=np.asarray(Image.open(folder/'native_4x.png').convert('RGBA')).astype(np.float32) if FULL_PART else None
    if INK_SPLIT:line_masks=line_cut_masks(art,big,rows)
    elif EDGE_RING:big=grow_labels(big,EDGE_RING)
    out=[]
    for k,r in enumerate(rows):
        x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h']
        piece=art[y*S:(y+h)*S,x*S:(x+w)*S].copy();mine=big[y*S:(y+h)*S,x*S:(x+w)*S]==k
        if line_masks is not None:mine=line_masks[k]
        if FULL_PART:
            # User 11/21 steps 3-4: cut the HD picture by the ORIGINAL part's own full shape and size
            # (the sprite's opaque pixels, enlarged smoothly), not by the pixels left visible in front
            # of its neighbours. Screen orientation here; flipped below with the piece.
            op=sprite_pixels(r)>0
            if r['flip_y']:op=op[::-1]
            if r['flip_x']:op=op[:,::-1]
            from PIL import Image as _I,ImageFilter as _F
            m=_I.fromarray((op*255).astype('uint8')).resize((w*S,h*S),_I.Resampling.BILINEAR).filter(_F.GaussianBlur(2))
            front=big[y*S:(y+h)*S,x*S:(x+w)*S]==k
            full=np.asarray(m)>=128
            # find the part in the HD picture (position and SCALE): Codex draws each pose freehand,
            # so the same original part sits a little elsewhere and bigger/smaller per pose.
            piece=register_piece(art,native4,x,y,w,h,op)
            r=dict(r,_visible=float(front[full].mean()) if full.any() else 0.)
            mine=full&(piece[...,3]>0)
        piece[~mine]=0
        if r['flip_y']:piece=piece[::-1];mine=mine[::-1]
        if r['flip_x']:piece=piece[:,::-1];mine=mine[:,::-1]
        opaque=sprite_pixels(r)>0
        if r['flip_y']:opaque=opaque[::-1]
        if r['flip_x']:opaque=opaque[:,::-1]
        out.append((r,piece,mine,opaque))
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--only',type=Path);p.add_argument('--selftest',action='store_true');p.add_argument('--out',type=Path);p.add_argument('--drawing',default='candidate.png')
    a=p.parse_args()
    names=json.loads(a.only.read_text()) if a.only else sorted(d.name for d in a.root.iterdir() if d.is_dir() and (d/'contract.json').exists())
    out=a.out or a.root/('split_selftest' if a.selftest else 'split');(out/'parts').mkdir(parents=True,exist_ok=True)
    merged={};used=0
    for name in names:
        folder=a.root/name;src=folder/('native_4x.png' if a.selftest else a.drawing)
        if not src.exists():continue
        used+=1
        for r,piece,mine,opaque in cut(folder,Image.open(src)):
            h=r['hash'];share=mine.mean()
            if h not in merged:merged[h]=dict(art=np.zeros_like(piece),score=np.full(mine.shape,-1.),opaque=opaque,row=r)
            m=merged[h]
            if FULL_PART:
                # one pose gives the whole part: the pose where the part is least covered by others
                vis=r.get('_visible',0.)
                if vis>m.get('best',-1.):
                    m['best']=vis;m['art'][:]=0;m['art'][mine]=piece[mine];m['score'][:]=-1;m['score'][mine]=vis
                continue
            take=mine&(share>m['score'])
            m['art'][take]=piece[take];m['score'][take]=share
    report=[]
    for h,m in merged.items():
        Image.fromarray(m['art']).save(out/'parts'/f'{h}.png')
        (out/'cov').mkdir(exist_ok=True);Image.fromarray(((m['score']>=0)*255).astype('uint8')).save(out/'cov'/f'{h}.png')   # pixels some drawing gave (package keeps their alpha)
        need=np.repeat(np.repeat(m['opaque'],S,0),S,1);got=(m['score']>=0)&need
        report.append(dict(hash=h,binding_id=m['row']['binding_id'],w=m['row']['w'],h=m['row']['h'],coverage=round(float(got.sum()/max(need.sum(),1)),3)))
    if a.selftest:
        bad=0
        for name in names:
            folder=a.root/name
            if not (folder/'native_4x.png').exists():continue
            rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'));W,H=Image.open(folder/'native.png').size
            _,label=compose_canvas(rows,W,H);truth=np.asarray(Image.open(folder/'native_4x.png').convert('RGBA'))
            canvas=np.zeros_like(truth);big=np.repeat(np.repeat(label,S,0),S,1)
            for k,r in enumerate(rows):
                part=merged[r['hash']]['art'].copy()
                if r['flip_x']:part=part[:,::-1]
                if r['flip_y']:part=part[::-1]
                x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h'];sel=big[y*S:(y+h)*S,x*S:(x+w)*S]==k
                canvas[y*S:(y+h)*S,x*S:(x+w)*S][sel]=part[sel]
            vis=big>=0;diff=int((canvas[vis]!=truth[vis]).any(1).sum())
            if diff:bad+=1;print('MISMATCH',name,diff)
        print('selftest objects',used,'mismatched',bad)
    cov=[r['coverage'] for r in report]
    (out/'coverage.json').write_text(json.dumps(sorted(report,key=lambda r:r['coverage']),ensure_ascii=False,indent=1),encoding='utf-8')
    print('drawings',used,'sprites',len(report),'full coverage',sum(1 for c in cov if c>=.999),'mean coverage',round(float(np.mean(cov)),3) if cov else None)


if __name__=='__main__':main()
