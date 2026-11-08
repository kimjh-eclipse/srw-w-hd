
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json
from hd_core import Core,ROOT
from scripts.diagnostics.inspect_attract_resources import memory_chunk
from player_controls import pad_buttons,sdl_pad_mapping

def main():
    out=ROOT/'test_current/controller';out.mkdir(exist_ok=True)
    mapping=sdl_pad_mapping(dict(a='b0',b='b1',x='b2',y='b3',leftshoulder='b9',rightshoulder='b10',start='b6',back='b4',dpup='b11',dpdown='b12',dpleft='b13',dpright='b14'))
    assert pad_buttons({0,10},[],[],mapping)=={8,11}
    assert pad_buttons({0,9},[],[],mapping)=={8,10}
    assert pad_buttons({13},[.8,0],[],mapping)=={6}
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'saves');rows=[]
    try:
        for raw in (set(),{0},{10},{0,10}):
            core.buttons=pad_buttons(raw,[],[],mapping)
            for _ in range(2):core.run();core.audio.clear()
            core.save(out/'current.state');regs=memory_chunk(out/'current.state')['9REG'];value=int.from_bytes(regs[0x130:0x132],'little')&1023
            rows.append(dict(raw_buttons=sorted(raw),nds_keyinput=value));expected=1023-(1 if 0 in raw else 0)-(256 if 10 in raw else 0);assert value==expected,(raw,value,expected)
    finally:core.close()
    report=dict(ps4_mapping=mapping,chords=rows,simultaneous_r_a_reaches_nds=True,dpad_buttons_beat_stick_drift=True);(out/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
