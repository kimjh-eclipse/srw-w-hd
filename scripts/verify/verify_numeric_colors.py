"""Verify native compact and battle digits with every HP warning palette."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import json
import numpy as np
from PIL import Image
from hd_fonts import FontRenderer

def main():
    out=ROOT/'test_current/font'
    forecast=np.asarray(Image.open(out/'forecast_confirm_0.png').convert('RGB'))[192:384].copy()
    battle=np.asarray(Image.open(out/'combat_hud_native.png').convert('RGB'))[:192].copy()
    report=[]
    for kind,native,height,left,right in [('forecast',forecast,8,168,208),('battle',battle,16,56,96)]:
        for color in ['normal','red','yellow']:
            sample=native.copy();cell=sample[:height,left:right]
            if kind=='forecast':
                lo=cell.min(2);hi=cell.max(2);mask=(lo>=80)&(hi.astype('int16')-lo<8)
                light=cell.max(2)
            else:
                mask=(cell[:,:,1]>=232)&(cell[:,:,2]>=232)&(cell[:,:,0]>=80)
                light=cell[:,:,0]
            if color!='normal':
                cell[mask,0]=light[mask];cell[mask,1]=light[mask] if color=='yellow' else 0;cell[mask,2]=0
            renderer=FontRenderer();found=renderer.recognize(sample)
            expected=[(left+i*8,0,ch) for i,ch in enumerate('5000/')]
            assert all(p in found for p in expected),(kind,color,expected,found)
            image=Image.fromarray(sample).resize((960,720),Image.Resampling.NEAREST)
            renderer.compose(image,sample);image.save(out/f'numeric_{kind}_{color}.png')
            report.append(dict(scene=kind,palette=color,recognized='5000/',all_expected_positions=True))
    (out/'numeric_colors_verification.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))

if __name__=='__main__':main()
