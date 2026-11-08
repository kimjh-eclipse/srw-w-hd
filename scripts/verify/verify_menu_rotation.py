"""Replay every favorite carousel selection, including its moving frames."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/menu_card';r=HDRenderer();c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves')
    sheet=Image.new('RGB',(1440,1080));report=[]
    try:
        c.load(ROOT/'test_current/formation/formation.state');c.run()
        for selection in range(9):
            if selection:
                for tick in range(64):
                    c.buttons={7} if tick<3 else set();c.run();c.audio.clear()
                    if tick in (3,10,25):
                        frame=r.render_top(c.native,c.ids,c.hd,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds)
                        assert r.menu_scene.last_scene=='favorite',(selection,tick)
            image=r.render_top(c.native,c.ids,c.hd,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds)
            assert r.menu_scene.last_scene=='favorite',selection
            image.save(out/f'rotation_{selection}.png');sheet.paste(image.resize((480,360),Image.Resampling.LANCZOS),((selection%3)*480,(selection//3)*360))
            report.append(dict(selection=selection,scene=r.menu_scene.last_scene,recognized_parts=sum(int(row[0]) in r.menu_scene.spec['favorite_bindings'] for row in c.parts)))
        sheet.save(out/'rotation_contact.png');(out/'rotation_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:c.close();r.parts_renderer.close();r.scenario_backgrounds.close()

if __name__=='__main__':main()
