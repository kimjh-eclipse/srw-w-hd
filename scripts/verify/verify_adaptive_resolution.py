"""Exercise live compositor size changes with portraits, cut-ins, menus and maps."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
from pathlib import Path
import numpy as np
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/performance';r=HDRenderer();c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'resolution_saves');report=[]
    try:
        for state in ['formation/formation.state','font/cutin_dialogue.state','scenario/final.state','map_icons/all_enemies_visible.state','localized_screens/chapter.state']:
            c.load(ROOT/'test_current'/state);c.run()
            for width in (1440,960,640,1440):
                r.set_resolution(width);start=time.perf_counter()
                top=r.render_top(c.native,c.ids,c.hd,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds)
                bottom=r.render_bottom(c.native,c.hd);assert top.size==bottom.size==(width,width*3//4)
                for target,source in [(top,c.native[:192]),(bottom,c.native[192:])]:
                    if np.any(source):assert np.asarray(target).max()>0,(state,width)
                if width==960:
                    name=Path(state).stem;top.save(out/(name+'_960_top.png'));bottom.save(out/(name+'_960_bottom.png'))
                report.append(dict(scene=state,width=width,height=width*3//4,render_ms=round((time.perf_counter()-start)*1000,2)))
        (out/'adaptive_resolution.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:r.set_resolution(1440);c.close();r.parts_renderer.close();r.backgrounds.close();r.scenario_backgrounds.close();r.map_icons.close()

if __name__=='__main__':main()
