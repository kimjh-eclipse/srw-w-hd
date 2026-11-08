"""Replay ordinary controller inputs to inspect the remaining weapon poses."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from PIL import Image
from hd_core import Core,ROOT

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'menu_saves')
    def step(button=None):
        for i in range(36):c.buttons={button} if button is not None and i<4 else set();c.run();c.audio.clear()
    def capture(name):Image.fromarray(c.native).save(out/(name+'.png'));c.save(out/(name+'.state'))
    try:
        c.load(ROOT/'test_current/map_icons/all_enemies_visible.state');step();capture('attack_cursor')
        step(5);step(5);capture('attack_unit')
        step(8);capture('attack_commands')
        step(5);step(8);capture('attack_weapons')
    finally:c.close()

if __name__=='__main__':main()
