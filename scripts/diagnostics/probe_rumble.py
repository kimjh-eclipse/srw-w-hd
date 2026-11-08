"""Read-only HP candidates in the canonical preview; no ROM edits."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json
import numpy as np
from hd_core import Core,ROOT,HERE
out=ROOT/'test_current/combat';out.mkdir(exist_ok=True)
core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True)
core.load(HERE/'demo.state',refresh_code=True)
core.api.retro_get_memory_data.argtypes=[C.c_uint];core.api.retro_get_memory_data.restype=C.c_void_p
ram=core.api.retro_get_memory_data(2);events=json.loads((HERE/'demo_input.json').read_text());candidates=None;trace=[]
for frame in range(64700,68001):
    core.buttons={e['button'] for e in events if e['from']<=frame<e['to']};core.run();core.audio.clear()
    if frame==65040:
        mem=np.frombuffer(C.string_at(ram,4*1024*1024),dtype='<u2');candidates=np.flatnonzero((mem==4400)|(mem==5000));last=mem[candidates].copy()
        trace.append(dict(frame=frame,initial={hex(0x2000000+int(i)*2):int(mem[i]) for i in candidates}))
    if candidates is not None:
        values=np.array([C.c_uint16.from_address(ram+int(i)*2).value for i in candidates]);changed=np.flatnonzero(values!=last)
        if len(changed):trace.append(dict(frame=frame,changes={hex(0x2000000+int(candidates[i])*2):[int(last[i]),int(values[i])] for i in changed}));last=values
core.close();(out/'rumble_hp_probe.json').write_text(json.dumps(trace,indent=2));print(json.dumps(trace)[:10000])
