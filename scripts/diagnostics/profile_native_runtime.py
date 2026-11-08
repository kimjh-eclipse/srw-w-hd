
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import time,json
import numpy as np
from hd_core import Core,ROOT
from frame_compositor import ReadyParts

def main():
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/parts/profile_saves');results=[]
    try:
        for enabled,ready in ((False,[]),(True,[]),(True,list(range(1,90000)))):
            proxy=ReadyParts();proxy.values=ready;proxy.ready_generation=len(ready)+int(enabled);core.load(ROOT/'test_current/attract/target.state');core.set_hd(enabled);core.set_ready_parts(proxy);times=[]
            for i in range(180):
                start=time.perf_counter();core.run();core.audio.clear();times.append((time.perf_counter()-start)*1000)
            row=dict(hd=enabled,ready=len(ready),mean_ms=float(np.mean(times)),p95_ms=float(np.percentile(times,95)),max_ms=max(times),obj_matches=int((core.parts[:,0]>0).sum()),bg_matches=int((core.bgparts[:,0]>0).sum()));results.append(row);print(row,flush=True)
    finally:core.close()
    (ROOT/'test_current/parts/native_profile.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
