
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,numpy as np
from hd_core import Core,ROOT
from frame_compositor import ReadyParts
n=int(sys.argv[1]);core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/parts/cadence_saves',frameskip=n);core.set_ready_parts(ReadyParts());core.load(ROOT/'test_current/attract/target.state')
try:
    for i in range(54):
        changed=core.run();core.audio.clear()
        if i==53 and (n==0 or changed):np.savez_compressed(ROOT/f'test_current/parts/cadence_{n}_{i}.npz',native=core.native,parts=core.parts,bgparts=core.bgparts,ids=core.ids,owners=core.owners,palettes=core.part_palettes,attrs=np.frombuffer(core.obj.raw,dtype='uint8'))
finally:core.close()
