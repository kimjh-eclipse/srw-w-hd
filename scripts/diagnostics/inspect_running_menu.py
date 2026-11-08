
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,ctypes as C
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_fonts import FontRenderer
from hd_renderer import HDRenderer

c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=True,demo=True,user_dir=ROOT/'test_current/font/saves')
r=FontRenderer();rows=[]
renderer=HDRenderer(async_parts=False,dynamic_parts=False,gpu_composition=True)
try:
    c.load(ROOT/'test_current/combat/sandrock_weapons.state')
    count=len(json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())['bindings'])
    values=(C.c_uint*count)(*range(1,count+1));c.api.retro_srw_set_ready_parts(values,count)
    for frame in range(120):
        c.run();c.audio.clear();native=c.native[:192].copy();r.recognize(native)
        rows.append(dict(frame=frame,selected=list(r.menu_glyphs),repairs=r.menu_repairs))
        if frame in (0,30,119):
            im=Image.fromarray(native).resize((768,576));r.compose(im,native);im.save(ROOT/f'test_current/font/running_menu_{frame}.png')
            renderer.set_resolution(768)
            im=renderer.render_top(c.native,c.ids,tuple(c.hd),False,parts=c.parts,owners=c.owners,obj=bytes(c.obj.raw),bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds,bg_layout=c.bg_layout)
            im.to_pil().save(ROOT/f'test_current/font/running_menu_gpu_{frame}.png')
    (ROOT/'test_current/font/running_menu.json').write_text(json.dumps(rows))
finally:c.close()
