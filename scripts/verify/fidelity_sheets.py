"""Side-by-side re-review sheets: for every accepted pose of a unit, native x4 (nearest) | drawing,
same scale, on a mid-blue background, labelled. One PNG per unit (pages of 8 poses).
Out: test_current/parts/pose_packets/_rereview/unit_<U>_<page>.png

  py -3.11 -X utf8 scripts/verify/fidelity_sheets.py [--units 74,11]
"""
import argparse,json,sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets';OUT=BASE/'_rereview'
CELL=330


def unit(rs):
    st=rs/'DRAWINGS_STATUS.json'
    if not st.exists():return rs.parent.name,0
    acc=sorted(k for k,v in json.loads(st.read_text(encoding='utf-8')).items() if v.get('state')=='accepted')
    pairs=[]
    for k in acc:
        f=rs/k
        if not ((f/'native_4x.png').exists() and (f/'candidate_fit.png').exists()):continue
        n=Image.open(f/'native_4x.png').convert('RGBA');d=Image.open(f/'candidate_fit.png').convert('RGBA')
        bb=n.getbbox() or (0,0,n.width,n.height);n=n.crop(bb);d=d.crop(bb)
        s=min(CELL/n.width,CELL/n.height,1.5);sz=(max(1,int(n.width*s)),max(1,int(n.height*s)))
        pairs.append((k,n.resize(sz,Image.NEAREST),d.resize(sz,Image.LANCZOS)))
    pages=0
    for p in range(0,len(pairs),8):
        chunk=pairs[p:p+8];cols=2
        sheet=Image.new('RGBA',(cols*(2*CELL+30),((len(chunk)+cols-1)//cols)*(CELL+22)),(235,235,235,255));dr=ImageDraw.Draw(sheet)
        for j,(k,n,d) in enumerate(chunk):
            x=(j%cols)*(2*CELL+30);y=(j//cols)*(CELL+22)
            for m,im in enumerate((n,d)):
                bg=Image.new('RGBA',(CELL,CELL),(40,60,150,255));bg.alpha_composite(im,((CELL-im.width)//2,(CELL-im.height)//2));sheet.alpha_composite(bg,(x+m*(CELL+4),y+20))
            dr.text((x+3,y+3),f'{rs.parent.name} {k}   native x4 | drawing',fill=(0,0,0))
        sheet.convert('RGB').save(OUT/f'{rs.parent.name}_{p//8:02d}.png');pages+=1
    return rs.parent.name,pages


def main():
    p=argparse.ArgumentParser();p.add_argument('--units',default='');a=p.parse_args()
    OUT.mkdir(exist_ok=True)
    sets=[rs for rs in sorted(BASE.glob('unit_*/robot_set')) if (rs/'INSTALLED').exists()]
    if a.units:sets=[BASE/f'unit_{u}/robot_set' for u in a.units.split(',')]
    with ProcessPoolExecutor(6) as ex:
        res=dict(ex.map(unit,sets))
    print('units',len(res),'pages',sum(res.values()))


if __name__=='__main__':main()
