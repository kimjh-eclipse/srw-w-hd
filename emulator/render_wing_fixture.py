"""Render both displays from a real saved Wing battle/menu state."""
import sys
from pathlib import Path
from PIL import Image
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    state=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'test_current/combat/sandrock_weapons.state'
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/wing_saves');r=HDRenderer()
    try:
        c.load(state);c.run();sub=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities)
        top=r.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds,bg_layout=c.bg_layout,sub_parts=sub)
        bottom=r.render_bottom(c.native,c.hd);top.save(ROOT/'test_current/combat/wing_top_hd.png');bottom.save(ROOT/'test_current/combat/wing_bottom_hd.png')
        print('parts',int((c.parts[:,0]>0).sum()),'subparts',int((c.sub_parts[:,0]>0).sum()),'cutin',list(c.hd)[:6])
        print('preparation',r.parts_renderer.registration_stats)
    finally:c.close();r.parts_renderer.close()

if __name__=='__main__':main()
