"""Unlock the morale-gated MAP weapon in an isolated verification state only.

The canonical ROM and player saves are never changed. This fixture raises
Duo's current morale from 111 to the native weapon's required 120.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json
from PIL import Image
from hd_core import Core,ROOT

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'wing_saves')
    def steps(buttons,frames):
        c.buttons=set(buttons)
        for _ in range(frames):c.run();c.audio.clear()
        c.buttons=set()
    try:
        c.load(out/'duo_map_locked.state');ram=c.api.retro_get_memory_data(2);address=0x1eb284
        before=C.c_uint16.from_address(ram+address).value
        assert before==111,before
        C.c_uint16.from_address(ram+address).value=120
        steps([0],5);steps([],25);steps([8],5);steps([],25);steps([5],5);steps([],25)
        c.save(out/'duo_map_unlocked.state');Image.fromarray(c.native).save(out/'duo_map_unlocked.png')
        (out/'duo_map_fixture.json').write_text(json.dumps(dict(test_only=True,rom_modified=False,player_saves_modified=False,memory_offset=hex(address),before=before,after=120),indent=2))
    finally:c.close()

if __name__=='__main__':main()
