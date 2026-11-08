"""Verify selected text after asynchronous dynamic parts become ready."""
import json,time
import numpy as np
from hd_core import Core,ROOT
from frame_compositor import FrameCompositor
from hd_fonts import FontRenderer

def main():
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=True,demo=True,user_dir=ROOT/'test_current/font/saves')
    renderer=FrameCompositor(async_parts=True,dynamic_parts=True)
    try:
        reports=[]
        for fixture in ('combat/sandrock_weapons.state','font/menu_alpha.state','combat/attack_commands.state'):
            c.load(ROOT/'test_current'/fixture)
            for step in range(12):
                for _ in range(4):c.run();c.audio.clear()
                image=renderer.capture(c,False)
                c.set_ready_parts(renderer.ready)
                time.sleep(.1)
            image.save(ROOT/f'test_current/font/runtime_{fixture.split("/")[-1]}.png')
            selected=[]
            for screen in (0,1):
                font=FontRenderer();font.recognize(c.native[screen*192:(screen+1)*192]);selected.extend(font.menu_repairs)
            assert selected,(fixture,'selection background vanished after dynamic texture replacement')
            reports.append(dict(fixture=fixture,selected_repairs=selected,ready_parts=len(renderer.ready.values)))
        (ROOT/'test_current/font/menu_runtime.json').write_text(json.dumps(reports,indent=2))
        print(reports,flush=True)
    finally:renderer.close();c.close()

if __name__=='__main__':main()
