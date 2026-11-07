"""Capture actual scene layers for the missing map and story backgrounds."""
import json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
import inspect_attract_resources as inspect

def main():
    out=ROOT/'test_current/scene_assets';out.mkdir(exist_ok=True)
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves')
    sheet=Image.new('RGB',(1024,1152));d=ImageDraw.Draw(sheet)
    states=['font/map_fresh.state','font/menu_step_0.state','font/menu_step_1.state','font/menu_step_2.state','font/menu_step_3.state','font/menu_step_4.state','font/menu_step_5.state','font/grid.state','scenario/final.state','formation/current.state','controller/current.state','formation/formation.state']
    try:
        for i,state in enumerate(states):
            c.load(ROOT/'test_current'/state);c.run();x=i%4*256;y=i//4*384
            sheet.paste(Image.fromarray(c.native),(x,y));d.text((x,y),state,fill='red')
            if i in (0,1,7,10):
                target=out/str(i);target.mkdir(exist_ok=True);inspect.OUT=target;inspect.snapshot(c,0)
                np.savez_compressed(target/'frame.npz',native=c.native,ids=c.ids,parts=c.parts,owners=c.owners,hd=np.array(c.hd))
        sheet.save(out/'scene_contact.png')
    finally:c.close()

if __name__=='__main__':main()
