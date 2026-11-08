"""Check foreground cut-ins against native second-target blend weights."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from hd_core import Core,ROOT
from hd_renderer import HDRenderer
from native_composition import PartVisibility

def main():
    layers=np.ones((192,256),dtype='uint8')
    v=PartVisibility(layers,np.zeros_like(layers),np.array([0,1,2,3,4,4],dtype='uint8'),np.zeros(128,dtype='uint16'))
    for weight in (0,8,16):
        for kind,item,control in ((0,0,0x3c42),(1,2,0x442)):
            out,_=v.mask(0,0,4,4,2,kind,item,control,weight<<8)
            assert np.all(out==255*weight//16),(kind,weight,out)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/saves')
    renderer=HDRenderer(gpu_composition=True);rows=[]
    try:
        for name in ('getter','golion'):
            core.load(ROOT/f'test_current/combat/{name}_cutin.state');core.run()
            kw=dict(parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds)
            image=renderer.render_top(core.native,core.ids,core.hd,**kw)
            image.save(ROOT/f'test_current/combat/{name}_cutin_fixed.png')
            attrs=np.frombuffer(core.obj.raw,dtype='<u2').reshape(128,4)
            visibility=PartVisibility(core.ids,core.owners,core.bgpriors,(attrs[:,2]>>10)&3);total=0
            for i in np.flatnonzero(core.parts[:,0]):
                row=core.parts[i];args=(0,0,256,192,int(row[3])>>10&3,0,int(i),int(row[7]))
                old,_=visibility.mask(*args);new,_=visibility.mask(*args,int(row[6]))
                total+=int(np.count_nonzero(old>new))
            assert total>0
            rows.append(dict(scene=name,blend_registers=sorted(set(int(row[6]) for row in core.parts if row[0])),foreground_samples_previously_overpainted=total))
        report=dict(actual_scenes=rows,second_target_weights=[0,8,16],obj_and_bg_weights_verified=True)
        (ROOT/'test_current/combat/cutin_blend_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:
        core.close();renderer.parts_renderer.close();renderer.backgrounds.close();renderer.scenario_backgrounds.close();renderer.map_icons.close()

if __name__=='__main__':main()
