"""Exercise cold texture preparation without blocking native emulation."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
import numpy as np
from PIL import Image
from hd_core import Core,ROOT,HERE
from hd_parts import PartsRenderer

def main():
    out=ROOT/'test_current/parts';out.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True)
    r=PartsRenderer(async_prepare=True);r.registered_cache=None
    r.prepare_delay=.25
    core.load(HERE/'demo.state',refresh_code=True)
    events=json.loads((HERE/'demo_input.json').read_text());fallback=ready=0;times=[]
    try:
        for f in range(64700,65601):
            core.buttons={e['button'] for e in events if e['from']<=f<e['to']}
            r.collect_prepared();core.set_ready_parts(r);core.run();core.audio.clear()
            if f%2:continue
            start=time.perf_counter()
            top=Image.fromarray(core.native[:192]).resize((1440,1080),Image.Resampling.NEAREST)
            r.compose(top,core.parts,core.obj.raw,core.ids,core.owners,core.bgpriors,core.bgparts,core.part_palettes)
            times.append((time.perf_counter()-start)*1000)
            active=core.parts[core.parts[:,0]>0]
            fallback+=int(np.count_nonzero(active[:,7]&0x80000000));ready+=int(np.count_nonzero((active[:,7]&0x80000000)==0))
        result=dict(render_median_ms=float(np.median(times)),render_p99_ms=float(np.percentile(times,99)),render_max_ms=max(times),native_fallback_parts=fallback,ready_hd_parts=ready,prepared=len(r.prepared),pending=len(r.pending),errors=r.prepare_errors)
        assert fallback>0 and ready>0,result
        assert np.percentile(times,99)<100,result
        assert not r.prepare_errors,result
        (out/'async_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
    finally:r.close();core.close()

if __name__=='__main__':main()
