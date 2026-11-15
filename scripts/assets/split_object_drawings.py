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


def cut(folder,drawing):
    rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'))
    native=Image.open(folder/'native.png');W,H=native.size
    _,label=compose_canvas(rows,W,H)
    art=np.asarray(drawing.convert('RGBA'))
    assert art.shape[:2]==(H*S,W*S),(folder.name,art.shape,(H*S,W*S))
    big=np.repeat(np.repeat(label,S,0),S,1)
    out=[]
    for k,r in enumerate(rows):
        x,y,w,h=r['screen_x'],r['screen_y'],r['w'],r['h']
        piece=art[y*S:(y+h)*S,x*S:(x+w)*S].copy();mine=big[y*S:(y+h)*S,x*S:(x+w)*S]==k
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
            m=merged[h];take=mine&(share>m['score'])
            m['art'][take]=piece[take];m['score'][take]=share
    report=[]
    for h,m in merged.items():
        Image.fromarray(m['art']).save(out/'parts'/f'{h}.png')
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
