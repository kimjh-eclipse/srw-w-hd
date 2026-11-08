"""Real menu selections must preserve unrelated pixels and restore green ink beds."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_fonts import FontRenderer

def main():
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=ROOT/'test_current/font/saves')
    reports=[];panels=[]
    try:
        for fixture,choices in (('font/forecast_confirm.state',4),('combat/attack_weapons.state',5),('combat/attack_commands.state',5)):
            c.load(ROOT/'test_current'/fixture)
            for selection in range(choices):
                for _ in range(15):c.run();c.audio.clear()
                native=c.native[192:].copy();r=FontRenderer();r.recognize(native);healed=r._heal_native(native)
                assert np.array_equal(native[~r.last_mask],healed[~r.last_mask]),(fixture,selection,'unrelated pixels changed')
                checked=0
                for left,top,right,bottom,sl,sr in r.menu_repairs:
                    for y in range(top,bottom):
                        values=native[y,sl:sr].astype('int16');green=(values[:,1]>values[:,0]+16)&(values[:,1]>values[:,2]+16)
                        if np.count_nonzero(green)<4:continue
                        erased=r.last_mask[y,left:right]
                        if not erased.any():continue
                        sample=healed[y,left:right][erased].astype('int16')
                        assert ((sample[:,1]>sample[:,0]+16)&(sample[:,1]>sample[:,2]+16)).all(),(fixture,selection,'shadow rectangle remains')
                        checked+=len(sample)
                image=Image.fromarray(native).resize((768,576),Image.Resampling.NEAREST);r.compose(image,native)
                panel=image.resize((384,288));ImageDraw.Draw(panel).text((2,274),f'{fixture} / {selection}',fill='yellow');panels.append(panel)
                reports.append(dict(scene=fixture,selection=selection,restored_green_pixels=checked,selected_glyphs=len(r.menu_glyphs),unrelated_pixels_unchanged=True))
                c.buttons={5}
                for _ in range(5):c.run();c.audio.clear()
                c.buttons=set()
        assert sum(x['restored_green_pixels']>0 for x in reports)>=8
        sheet=Image.new('RGB',(384*4,288*((len(panels)+3)//4)))
        for i,panel in enumerate(panels):sheet.paste(panel,(i%4*384,i//4*288))
        sheet.save(ROOT/'test_current/font/menu_background_audit.png')
        (ROOT/'test_current/font/menu_background_audit.json').write_text(json.dumps(reports,indent=2));print(json.dumps(reports))
    finally:c.close()

if __name__=='__main__':main()
