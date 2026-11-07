import ctypes as C,json
import numpy as np
from hd_core import Core,ROOT,HERE
core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True);core.load(HERE/'demo.state',refresh_code=True)
core.api.retro_srw_copy_obj_debug.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
core.api.retro_get_memory_data.argtypes=[C.c_uint];core.api.retro_get_memory_data.restype=C.c_void_p
ram=core.api.retro_get_memory_data(2);oam=np.zeros((128,4),dtype='uint16');pal=np.zeros((16,16),dtype='uint16');regs=np.zeros(64,dtype='uint16')
events=json.loads((HERE/'demo_input.json').read_text());pals=[];attrs=[];states=[]
for frame in range(64700,68001):
    core.buttons={e['button'] for e in events if e['from']<=frame<e['to']};core.run();core.audio.clear()
    core.api.retro_srw_copy_obj_debug(oam.ctypes.data,pal.ctypes.data,regs.ctypes.data)
    pals.append(pal.copy());attrs.append(oam.copy());states.append([C.c_uint32.from_address(ram+0xa6f38).value,C.c_uint32.from_address(ram+0x1e7a10).value,C.c_uint32.from_address(ram+0x1f729c).value])
core.close();np.savez_compressed(ROOT/'test_current/combat/battle_feedback.npz',palettes=pals,oam=attrs,states=states,start=64700)
print('feedback saved')
