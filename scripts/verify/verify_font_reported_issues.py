"""Regress selected-button bounds and the reported colored battle HUD digits."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image
from hd_fonts import FontRenderer,ROOT

def main():
    folder=ROOT/'test_current/font';native=np.asarray(Image.open(folder/'combat_hud_native.png').convert('RGB'))[:192]
    menu=np.asarray(Image.open(folder/'forecast_confirm_0.png').convert('RGB'))[192:384]
    report=dict(widths=[],menu_outline_removed=True,all_battle_digits=True,cyan_background_wildcards=True)
    for width in (768,960,1440):
        r=FontRenderer();size=(width,width*3//4)
        target=Image.fromarray(menu).resize(size,Image.Resampling.NEAREST);r.compose(target,menu)
        assert {(116,96),(128,96)}<=r.menu_glyphs
        for char in ('전','투'):
            cell=r._glyph(char,round(12*width/256),round(12*width/256),(255,255,255,255),button=True)
            pixels=np.asarray(cell);ys,xs=np.nonzero(pixels[:,:,3]);assert ys.min()>0 and ys.max()<cell.height-1
            assert np.all(pixels[ys,xs,:3]==255),'selected font has a dark stroke'
        r=FontRenderer();found=r.recognize(native);line=[ch for x,y,ch in sorted(found) if y==0]
        assert ''.join(line)=='HP5000/5000EN170/170',line
        assert not any(ch=='·' for x,y,ch in found if y<24)
        # Every ROM digit is also checked over colored stars in transparent
        # source pixels, which must not invalidate an otherwise exact match.
        sample=native.copy();sample[:16,40:144]=[0,0,180]
        sample[0:4,40:144:3]=[200,255,255]
        with np.load(ROOT/'graphics/fonts/battle_hud_glyphs.npz') as archive:
            for index,(indices,ch) in enumerate(zip(archive['indices'],archive['characters'])):
                x=40+8*index;cell=sample[:16,x:x+8];opaque=indices>0
                colors=np.zeros((16,3),dtype='uint8');colors[1]=[49,48,98];colors[13]=[230,255,255];colors[14]=[180,255,255];colors[15]=[131,255,255]
                cell[opaque]=colors[indices[opaque]]
        r=FontRenderer();found=r.recognize(sample)
        for index,ch in enumerate('0123456789/?'):assert (40+8*index,0,ch) in found,(width,index,ch)
        target=Image.fromarray(sample).resize(size,Image.Resampling.NEAREST);r.compose(target,sample)
        report['widths'].append(width)
    (folder/'reported_issues_verification.json').write_text(json.dumps(report,indent=2));print(report)

if __name__=='__main__':main()
