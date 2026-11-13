"""Assert classified VFX keep their native picture while no HD binding is ready."""
import json,queue,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core

class NotReady:
    ready_generation=0
    dynamic_bindings=queue.SimpleQueue()
    def ready_bindings(self):return []

def main():
    out=ROOT/'test_current/parts/effect_guard_review'
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'unready_saves')
    seen=unexpected=0
    try:
        assert core.effect_bridge,'Select a core with the effect classification API'
        core.load(ROOT/'test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1610_capture/frame_600.state')
        core.set_ready_parts(NotReady());ids=set(core.effect_part_ids)
        for _ in range(180):
            core.run();core.audio.clear()
            for row in core.parts:
                if int(row[0]) in ids:
                    seen+=1
                    if not int(row[7])&0x80000000:unexpected+=1
        report=dict(core=core.core_path,effect_bridge=core.effect_bridge,classified_effects=len(ids),observed_unready_effects=seen,incorrectly_hidden_native_effects=unexpected)
        (out/'unready_result.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
        assert seen and not unexpected
    finally:core.close()

if __name__=='__main__':main()
