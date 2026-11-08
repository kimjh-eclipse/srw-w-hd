"""Inspect selected text backgrounds on both native displays."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sys,ctypes as C
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from hd_fonts import FontRenderer

def main():
    out=ROOT/'test_current/font';enabled='--hd' in sys.argv;c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=enabled,demo=True,user_dir=out/'saves');panels=[];reports=[]
    if enabled:
        count=len(json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())['bindings']);values=(C.c_uint*count)(*range(1,count+1));c.api.retro_srw_set_ready_parts(values,count)
    try:
        for fixture in ('font/map_fresh.state','font/menu_alpha.state','combat/attack_commands.state','combat/sandrock_weapons.state'):
            c.load(ROOT/'test_current'/fixture);c.refresh_video();c.audio.clear()
            for screen in range(2):
                native=c.native[screen*192:(screen+1)*192].copy();r=FontRenderer();r.recognize(native)
                image=Image.fromarray(native).resize((768,576),Image.Resampling.NEAREST);r.compose(image,native)
                panel=image.resize((384,288));ImageDraw.Draw(panel).text((2,274),f'{fixture} screen {screen}',fill='yellow');panels.append(panel)
                reports.append(dict(fixture=fixture,screen=screen,selected=list(r.menu_glyphs),repairs=r.menu_repairs,runs=r.menu_runs))
                Image.fromarray(native).save(out/f'menu_inspect_{len(reports)-1}_native.png')
        sheet=Image.new('RGB',(768,288*4))
        for n,p in enumerate(panels):sheet.paste(p,(n%2*384,n//2*288))
        sheet.save(out/'menu_inspect.png');(out/'menu_inspect.json').write_text(json.dumps(reports,indent=2));print([(x['fixture'],x['screen'],x['selected'],x['repairs']) for x in reports])
    finally:c.close()

if __name__=='__main__':main()
