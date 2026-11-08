"""Capture a deterministic native attack phase from an in-game weapon menu."""
import sys,ctypes as C
from hd_core import Core,ROOT
from PIL import Image

def main():
    pilot=sys.argv[1];weapon=int(sys.argv[2]);wanted=int(sys.argv[3]);out=ROOT/'test_current/combat'
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'wing_saves')
    def steps(buttons,frames):
        c.buttons=set(buttons)
        for _ in range(frames):c.run();c.audio.clear()
        c.buttons=set()
    try:
        c.load(out/(pilot+'_weapons.state'));steps([],15)
        if weapon!=1:steps([4 if weapon==0 else 5],5);steps([],15)
        steps([8],5);steps([],40)
        if pilot=='duo':steps([7],1);steps([],10);steps([7],1);steps([],10);steps([4],1);steps([],10)
        steps([8],5);steps([],40)
        if pilot=='duo':steps([8],5);steps([],40)
        ram=c.api.retro_get_memory_data(2)
        for frame in range(wanted+1):
            c.run();c.audio.clear()
            active=C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0
            c.buttons={11,8} if active and frame%120<5 else set()
        name=sys.argv[4] if len(sys.argv)>4 else ('quatre' if pilot=='sandrock' else pilot)
        c.save(out/(name+'_cutin_full.state'));Image.fromarray(c.native).save(out/(name+'_cutin_full_native.png'))
    finally:c.close()

if __name__=='__main__':main()
