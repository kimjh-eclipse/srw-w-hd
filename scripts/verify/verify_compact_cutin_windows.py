"""Retain simultaneous pilot planes while rejecting stale compact texture uploads."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core


def main():
    folder=ROOT/'test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture'
    out=ROOT/'test_current/combat/mazinger_combination';out.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    results=[]
    try:
        assert hasattr(core.api,'retro_srw_register_cutin_map_windows'),'Production core lacks full SCR guard'
        for frame,expected in ((360,{171,172}),(720,{175,177,178}),(1320,set())):
            core.load(folder/f'frame_{frame}.state');core.run();core.audio.clear()
            active={int(row[0]) for row in core.cutin_layers if row[0]}
            assert active==expected,(frame,active,expected)
            results.append(dict(frame=frame,active=sorted(active),expected=sorted(expected)))
    finally:core.close()
    (out/'cutin_window_verification.json').write_text(json.dumps(dict(cases=results,passed=True),indent=2))
    print('Verified two positive multilayer states and stale-upload rejection')


if __name__=='__main__':main()
