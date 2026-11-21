"""Part-atlas redraw request for one unit (11/21): every unique robot sprite drawn ONCE, so all poses
share the same picture of a part.

test_current/parts/redraw_requests/unit_<U>/
  PART_ATLAS_native4x.png   the canvas Codex paints: each unique part at 4x (nearest) in its own box,
                            numbered; transparent outside the original pixels. Same size output wanted.
  PART_ATLAS_guide.png      the same with box outlines and numbers (reference only)
  ASSEMBLY_<pose>.png       native 4x of each pose with every part's box and number drawn on it, next to
                            the existing Codex drawing (style reference only)
  ATLAS.json                part number -> hash, size, atlas box, poses where it appears
  REQUEST.md                the direction text

  py -3.11 -X utf8 scripts/assets/build_part_redraw_request.py 196
"""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
S=4;PAD=24


def main():
    uid=int(sys.argv[1]);rs=ROOT/f'test_current/parts/pose_packets/unit_{uid}/robot_set'
    out=ROOT/f'test_current/parts/redraw_requests/unit_{uid}';out.mkdir(parents=True,exist_ok=True)
    st=json.loads((rs/'DRAWINGS_STATUS.json').read_text(encoding='utf-8'))
    poses=sorted(p.name for p in rs.glob('pose_[0-9]*') if (p/'contract.json').exists())
    parts={};seen={}
    for p in poses:
        for r in json.loads((rs/p/'contract.json').read_text(encoding='utf-8')):
            parts.setdefault(r['hash'],r);seen.setdefault(r['hash'],[]).append(p)
    order=sorted(parts,key=lambda h:(-parts[h]['w']*parts[h]['h'],h))
    num={h:i+1 for i,h in enumerate(order)}
    # shelf packing at 4x with padding
    W=1600;x=y=PAD;rowh=0;boxes={}
    for h in order:
        r=parts[h];w,hh=r['w']*S,r['h']*S
        if x+w+PAD>W:x=PAD;y+=rowh+PAD+18;rowh=0
        boxes[h]=(x,y+18,w,hh);x+=w+PAD;rowh=max(rowh,hh)
    H=y+rowh+PAD+18
    atlas=Image.new('RGBA',(W,H),(0,0,0,0));guide=Image.new('RGBA',(W,H),(235,235,235,255))
    try:fnt=ImageFont.truetype('malgun.ttf',14)
    except Exception:fnt=None
    dg=ImageDraw.Draw(guide)
    for h in order:
        r=parts[h];x,y,w,hh=boxes[h]
        idx=np.frombuffer(zlib.decompress(base64.b64decode(r['index_pixels'])),dtype='uint8').reshape(r['h'],r['w'])
        pal=np.array(r['original_palette_rgb'],dtype='uint8');rgba=np.dstack([pal[idx],(idx>0).astype('uint8')*255])
        im=Image.fromarray(rgba).resize((w,hh),Image.Resampling.NEAREST);atlas.alpha_composite(im,(x,y))
        bg=Image.new('RGBA',(w,hh),(40,60,150,255));bg.alpha_composite(im);guide.alpha_composite(bg,(x,y))
        dg.rectangle((x-1,y-1,x+w,y+hh),outline=(255,0,0));dg.text((x,y-17),f'#{num[h]} {r["w"]}x{r["h"]}',fill=(0,0,0),font=fnt)
    atlas.save(out/'PART_ATLAS_native4x.png');guide.convert('RGB').save(out/'PART_ATLAS_guide.png')
    for p in poses:
        rows=json.loads((rs/p/'contract.json').read_text(encoding='utf-8'))
        n=Image.open(rs/p/'native_4x.png').convert('RGBA');bg=Image.new('RGBA',n.size,(40,60,150,255));bg.alpha_composite(n);d=ImageDraw.Draw(bg)
        for r in reversed(rows):
            x,y=r['screen_x']*S,r['screen_y']*S;d.rectangle((x,y,x+r['w']*S-1,y+r['h']*S-1),outline=(255,60,60));d.text((x+2,y+1),f"#{num[r['hash']]}{'↔' if r['flip_x'] else ''}{'↕' if r['flip_y'] else ''}",fill=(255,255,0),font=fnt)
        tiles=[bg]
        if (rs/p/'candidate_fit.png').exists():
            c=Image.open(rs/p/'candidate_fit.png').convert('RGBA');b2=Image.new('RGBA',c.size,(40,60,150,255));b2.alpha_composite(c);tiles.append(b2)
        sheet=Image.new('RGB',(sum(t.width for t in tiles)+10*(len(tiles)-1),tiles[0].height),(255,255,255));xx=0
        for t in tiles:sheet.paste(t.convert('RGB'),(xx,0));xx+=t.width+10
        sheet.save(out/f'ASSEMBLY_{p}.png')
    (out/'ATLAS.json').write_text(json.dumps(dict(unit=uid,canvas=[W,H],scale=S,parts={str(num[h]):dict(hash=h,size=[parts[h]['w'],parts[h]['h']],box=boxes[h],poses=seen[h]) for h in order}),ensure_ascii=False,indent=1),encoding='utf-8')
    print('unit',uid,'parts',len(order),'poses',len(poses),'canvas',(W,H))


if __name__=='__main__':main()
