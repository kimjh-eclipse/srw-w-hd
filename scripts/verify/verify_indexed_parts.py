"""Exercise native index matching with RGB matches deliberately disabled."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json
import numpy as np
from hd_core import Core,ROOT,HERE
from hd_parts import PartsRenderer

library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())['bindings']
catalog=json.loads((ROOT/'graphics/all_units/catalog.json').read_text())['packages']
hero=next(p for p in catalog if p['resource']==3376);source={p['hash']:p for p in hero['parts']}
core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True)
core.load(HERE/'demo.state',refresh_code=True);events=json.loads((HERE/'demo_input.json').read_text())
for frame in range(64700,65042):
    core.buttons={e['button'] for e in events if e['from']<=frame<e['to']};core.run();core.audio.clear()
fixture=next(row.copy() for row in core.parts if row[0] and int(row[4]) in source)
part=source[int(fixture[4])];binding=int(fixture[0]);dummy=(C.c_uint*1)(0)
core.api.retro_srw_register_parts(dummy,0)
keys=(C.c_uint*1)(part['index_hash']);ids=(C.c_uint*1)(binding)
core.api.retro_srw_register_indexed_parts(keys,ids,1);core.run()
found=np.flatnonzero(core.parts[:,0]==binding);assert len(found)>0,'native index fallback did not find the part'
assert all(int(core.parts[i,4])==int(fixture[4]) for i in found)
pal=np.asarray(hero['palette_rgb'],dtype='uint32');five=(pal*31+127)//255
expected=(five[:,0]|(five[:,1]<<5)|(five[:,2]<<10)).astype('uint16')
assert np.array_equal(core.part_palettes[found[0],1:],expected[1:]),'render-time native palette was not copied'
core.set_hd(False);core.run();assert not core.parts[:,0].any();core.close()
renderer=PartsRenderer();index=next(i for i,b in enumerate(renderer.bindings,1) if b.get('dynamic_palette'))
spec=renderer.bindings[index-1];pal=np.asarray(spec['original_palette_rgb'],dtype='uint32');five=(pal*31+127)//255
colors=(five[:,0]|(five[:,1]<<5)|(five[:,2]<<10)).astype('uint16')
row=np.array([index,0,0,0,spec['hash'],0,0,0],dtype='uint32')
normal=np.array(renderer.sprite(row,bytes(1024),colors));row[4]=0
black=np.array(renderer.sprite(row,bytes(1024),np.zeros(16,dtype='uint16')))
assert np.array_equal(normal[:,:,3],black[:,:,3]),'palette change altered sprite geometry'
assert normal[:,:,:3][normal[:,:,3]>0].any() and not black[:,:,:3][black[:,:,3]>0].any()
result=dict(native_rgb_table_disabled=True,indexed_match=True,native_palette_capture=True,hd_off=True,black_fade_preserves_alpha=True)
(ROOT/'test_current/parts/indexed_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
