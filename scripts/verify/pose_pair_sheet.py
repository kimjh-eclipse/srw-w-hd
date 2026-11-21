"""Big native|drawing pairs for chosen (unit, pose) items, captioned. For verifying review calls.

  py -3.11 -X utf8 scripts/verify/pose_pair_sheet.py out.png unit_74:pose_00 unit_11:pose_03 ...
  items may carry a caption after '=' : unit_74:pose_00=white jaw
"""
import sys
from pathlib import Path
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets';C=420


def main():
    out=Path(sys.argv[1]);items=sys.argv[2:];cells=[]
    for it in items:
        key,_,cap=it.partition('=');u,p=key.split(':');f=BASE/u/'robot_set'/p
        try:n=Image.open(f/'native_4x.png').convert('RGBA');d=Image.open(f/'candidate_fit.png').convert('RGBA')
        except Exception:continue
        bb=n.getbbox() or (0,0,n.width,n.height);n=n.crop(bb);d=d.crop(bb);s=min(C/n.width,C/n.height,2.0)
        sz=(max(1,int(n.width*s)),max(1,int(n.height*s)));cells.append((f'{u} {p} {cap}'[:90],n.resize(sz,Image.NEAREST),d.resize(sz,Image.LANCZOS)))
    sheet=Image.new('RGB',(2*(2*C+30),((len(cells)+1)//2)*(C+24)),(235,235,235));dr=ImageDraw.Draw(sheet)
    for j,(t,n,d) in enumerate(cells):
        x=(j%2)*(2*C+30);y=(j//2)*(C+24)
        for m,im in enumerate((n,d)):
            bg=Image.new('RGBA',(C,C),(40,60,150,255));bg.alpha_composite(im,((C-im.width)//2,(C-im.height)//2));sheet.paste(bg.convert('RGB'),(x+m*(C+4),y+22))
        dr.text((x+3,y+4),t,fill=(0,0,0))
    sheet.save(out);print(out,len(cells))


if __name__=='__main__':main()
