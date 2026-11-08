"""Identify the isolated verification fixture's authoritative morale field."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json
from PIL import Image,ImageDraw
from hd_core import Core,ROOT

def main():
    out=ROOT/'test_current/combat';c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'wing_saves');panels=[];records=[]
    def steps(buttons,frames):
        c.buttons=set(buttons)
        for _ in range(frames):c.run();c.audio.clear()
        c.buttons=set()
    try:
        for address in (0x1eb284,0x1f15c2,0x1f15c4,0x1f15c6,0x1f284c,0x1f3aec):
            c.load(out/'duo_map_locked.state');ram=c.api.retro_get_memory_data(2);before=C.c_uint16.from_address(ram+address).value
            if before!=111:continue
            C.c_uint16.from_address(ram+address).value=120
            steps([0],5);steps([],25);steps([8],5);steps([],25);steps([5],5);steps([],25);steps([8],5);steps([],30)
            panel=Image.fromarray(c.native).resize((256,384));ImageDraw.Draw(panel).text((2,4),hex(address),fill='yellow');panels.append(panel);c.save(out/f'morale_{address:x}.state')
            records.append(dict(address=hex(address),after=C.c_uint16.from_address(ram+address).value))
        sheet=Image.new('RGB',(256*3,384*2))
        for n,panel in enumerate(panels):sheet.paste(panel,(n%3*256,n//3*384))
        sheet.save(out/'duo_morale_probe.png');(out/'duo_morale_probe.json').write_text(json.dumps(records,indent=2))
    finally:c.close()

if __name__=='__main__':main()
