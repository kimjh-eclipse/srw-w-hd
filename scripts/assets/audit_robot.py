"""Map supported robot poses across the whole demonstration battle."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json,struct,hashlib
from collections import Counter
from hd_core import Core,ROOT,HERE
from scripts.diagnostics.probe_robot import snapshot

out=ROOT/'test_current/robot';out.mkdir(exist_ok=True)
core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True);core.load(HERE/'demo.state',refresh_code=True)
events=json.loads((HERE/'demo_input.json').read_text());oam=C.create_string_buffer(1024);pal=C.create_string_buffer(512);regs=C.create_string_buffer(128);vram=C.create_string_buffer(0x4000)
expected=hashlib.sha256((out/'vram_65340.bin').read_bytes()[:0x4000]).digest();groups={};timeline=[]
for f in range(64700,67500):
    core.buttons={e['button'] for e in events if e['from']<=f<e['to']};core.run();core.audio.clear()
    core.api.retro_srw_copy_vram(0x06400000,vram,0x4000)
    if hashlib.sha256(vram.raw).digest()!=expected:continue
    core.api.retro_srw_copy_obj_debug(oam,pal,regs)
    parts=[]
    for i in range(128):
        a,b,c,_=struct.unpack_from('<4H',oam.raw,i*8)
        if not a&256 and not a&512 and c>>12==0:parts.append((a&0xff00,b&0xfe00,c))
    if not parts:continue
    key=str(parts)
    if key not in groups:
        groups[key]=dict(id=len(groups)+1,first=f,last=f,frames=0,parts=parts)
        snapshot(core,out,f)
    g=groups[key];g['last']=f;g['frames']+=1;timeline.append([f,g['id']])
core.close();report=dict(groups=list(groups.values()),timeline=timeline)
(out/'pose_audit.json').write_text(json.dumps(report,indent=2))
print([(g['id'],g['first'],g['last'],g['frames'],len(g['parts'])) for g in groups.values()])
