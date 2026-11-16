"""Cut a Codex unified sheet (unified_sheet/candidate_sheet.png + source_layout.json)
back into pose_NN/candidate.png.

Layout formats seen so far (all accepted):
  {"sheet":[W,H], "layout":[{"pose":"pose_00","sheet_origin":[x,y],"source_canvas":[w,h]}]}
  {"sheet_size":[W,H], "poses":[{"pose":"pose_00","source_rect_xywh":[x,y,w,h]}]}
  {"sheet_size":[W,H], "poses":[{"pose":0,"source_rect":[x0,y0,x1,y1]}]}
  {"size":[W,H], "poses":[{"pose":"pose_00","origin":[x,y],"size":[w,h]}]}
The drawing may be smaller than the sheet; it is scaled to the sheet size
first (aspect must match within 1%). An existing candidate.png is kept as
candidate_vN.png (candidate_fit.png as candidate_fit_vN.png).

  py -3.11 -X utf8 scripts/assets/split_unified_sheet.py <set dir> [candidate_sheet.png]
"""
import json,sys
from pathlib import Path
from PIL import Image


def entries(lay,root):
    items=lay.get('layout') or lay.get('poses')
    for e in items:
        p=e['pose'];name=p if isinstance(p,str) else f'pose_{int(p):02d}'
        if 'sheet_origin' in e:x,y=e['sheet_origin'];w,h=e['source_canvas']
        elif 'source_rect_xywh' in e:x,y,w,h=e['source_rect_xywh']
        elif 'source_rect' in e:x0,y0,x1,y1=e['source_rect'];x,y,w,h=x0,y0,x1-x0,y1-y0
        elif 'origin' in e:x,y=e['origin'];w,h=e.get('size') or e['canvas']
        else:raise KeyError(('unknown pose entry',e))
        # The cut must equal the pose canvas (native_4x.png) exactly.
        nw,nh=Image.open(root/name/'native_4x.png').size
        assert (w,h)==(nw,nh),(name,(w,h),(nw,nh))
        yield name,x,y,w,h


def main():
    root=Path(sys.argv[1]);name=sys.argv[2] if len(sys.argv)>2 else 'candidate_sheet.png'
    sheet=root/'unified_sheet';lay=json.loads((sheet/'source_layout.json').read_text(encoding='utf-8'))
    size=lay.get('sheet') if isinstance(lay.get('sheet'),list) else lay.get('sheet_size') or lay.get('size') or lay.get('source_sheet_size')
    W,H=size;art=Image.open(sheet/name).convert('RGBA')
    sx,sy=art.width/W,art.height/H
    assert abs(sx/sy-1)<.06,('aspect differs',art.size,(W,H))   # x and y are scaled separately; the fit corrects per pose
    gen=sheet/'generated_all_poses.png';gsize=Image.open(gen).size if gen.exists() else art.size
    print('drawing',art.size,'generated',gsize,'sheet',(W,H),'-> about',round(4*gsize[0]/W,2),'generated px per native px')
    if art.size!=(W,H):art=art.resize((W,H),Image.Resampling.LANCZOS)
    n_out=0
    for pose,x,y,w,h in entries(lay,root):
        dst=root/pose/'candidate.png'
        if dst.exists():
            n=1
            while (root/pose/f'candidate_v{n}.png').exists():n+=1
            dst.replace(root/pose/f'candidate_v{n}.png')
            fit=root/pose/'candidate_fit.png'
            if fit.exists():fit.replace(root/pose/f'candidate_fit_v{n}.png')
        art.crop((x,y,x+w,y+h)).save(dst);n_out+=1
    print('poses',n_out)


if __name__=='__main__':main()
