"""Replay each protagonist configuration selection through the real native menus."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from hd_renderer import HDRenderer
from scripts.diagnostics import inspect_attract_resources as inspect


def main():
    out=ROOT/'test_current/menu_card/configuration';out.mkdir(parents=True,exist_ok=True)
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    renderer=HDRenderer();renderer.set_resolution(768);rows=[]
    try:
        for name,steps in (('overview',0),('pilot',4),('aircraft',3),('warship',2),('weapon',1)):
            c.load(ROOT/'test_current/formation/favorite_base.state')
            for _ in range(steps):
                c.buttons={4}
                for _ in range(2):c.run();c.audio.clear()
                c.buttons=set()
                for _ in range(12):c.run();c.audio.clear()
            c.buttons=set()
            for _ in range(15):c.run();c.audio.clear()
            target=out/name;target.mkdir(exist_ok=True);inspect.OUT=target;inspect.snapshot(c,0);c.save(target/'current.state')
            image=renderer.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,
                owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,
                backgrounds=c.backgrounds,bg_layout=c.bg_layout)
            image.save(target/'hd.png');Image.fromarray(c.native).save(target/'native.png')
            rows.append(dict(selection=name,backgrounds=c.backgrounds,matched=renderer.backgrounds.last_matches,scene=renderer.menu_scene.last_scene,layout=c.bg_layout))
            print(name,rows[-1],flush=True)
        (out/'report.json').write_text(json.dumps(rows,indent=2))
    finally:c.close();renderer.parts_renderer.close()


if __name__=='__main__':main()
