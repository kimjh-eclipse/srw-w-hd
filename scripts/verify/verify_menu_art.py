
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/menu_card';r=HDRenderer()
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves')
    report={}
    try:
        for name,state in [('introduction','favorite_base.state'),('favorite','formation.state')]:
            c.load(ROOT/'test_current/formation'/state);c.run()
            image=r.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds)
            image.save(out/(name+'_hd_verified.png'))
            report[name]=dict(backgrounds=c.backgrounds,matched=r.backgrounds.last_matches,scene=r.menu_scene.last_scene,parts=[int(c.parts[i,0]) for i in range(19,46)])
            if name=='introduction':assert r.menu_scene.last_scene=='introduction',report[name]
            else:assert all(c.parts[i,0]>0 for i in range(19,46)),report[name]
        (out/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:c.close()

if __name__=='__main__':main()
