
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import numpy as np,json
from PIL import Image
from hd_core import Core,ROOT
from frame_compositor import ReadyParts
import scripts.diagnostics.inspect_attract_resources as inspector
out=ROOT/'test_current/formation';inspector.OUT=out
core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'boot_saves');core.set_ready_parts(ReadyParts());core.load(out/'current.state')
try:
    for f in range(3000):
        phase=f%160;core.buttons={3} if phase<3 else ({8,11} if 80<=phase<140 else set());core.run();core.audio.clear()
        a=core.native[:192].astype('int16');ratio=float(((a[:,:,1]>25)&(abs(a[:,:,1]-a[:,:,2])<20)&(a[:,:,0]<a[:,:,1]/2)).mean())
        if ratio>.25:
            core.buttons=set()
            for _ in range(30):core.run();core.audio.clear()
            core.save(out/'favorite_base.state');Image.fromarray(core.native).save(out/'favorite_base_native.png');inspector.snapshot(core,0);print('favorite',f,ratio,flush=True);break
    else:print('not found')
finally:core.close()
