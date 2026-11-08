"""Compare filtered and exhaustive identifiers on the same live battle frames."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import copy,json,time
from collections import OrderedDict
from hd_battle_backgrounds import BattleBackgroundRenderer
from hd_core import Core,ROOT,HERE

def main():
    fast=BattleBackgroundRenderer(async_prepare=False);fast.refresh()
    exhaustive=copy.copy(fast);exhaustive.palette_possible=None
    exhaustive.active_layers={};exhaustive.uv_corrections={};exhaustive.sample_plans=OrderedDict()
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/performance/filter_saves')
    core.load(ROOT/'test_current/font/cutin_dialogue.state',refresh_code=True)
    schedule=json.loads((HERE/'demo_input.json').read_text());samples=0;before=0;after=0;matches=0
    try:
        for frame in range(65272,66151):
            core.buttons={e['button'] for e in schedule if e['from']<=frame<e['to']};core.run();core.audio.clear()
            if frame<65500 or frame%4:continue
            rows=fast.battle_layers(core.bg_layout)
            for row in rows:
                start=time.perf_counter();a=exhaustive.identify(core.native,core.ids,row);before+=time.perf_counter()-start
                start=time.perf_counter();b=fast.identify(core.native,core.ids,row);after+=time.perf_counter()-start
                assert a==b,(frame,row,a,b)
                samples+=1;matches+=a is not None
    finally:core.close();fast.close()
    report=dict(samples=samples,identified=matches,identical_choices_and_uvs=True,exhaustive_ms=before*1000,filtered_ms=after*1000,speedup=before/after)
    (ROOT/'test_current/performance/background_filter_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
