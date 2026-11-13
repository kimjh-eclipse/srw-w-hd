"""Check DS alpha color arithmetic, priority ties, and GPU/Pillow parity."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from foreground_blend import blend_part,gpu_plane
from gpu_surface import Surface


def main():
    art=Image.new('RGBA',(16,16),(80,100,120,255))
    packed=np.full((16,16),31|(1<<15)|(8<<18)|(8<<23)|(16<<32)|(5<<37),dtype='uint64')
    eligible=np.ones((16,16),dtype=bool)
    result=np.asarray(blend_part(art,packed,eligible,(1,0,0,0,1,0)))
    assert tuple(result[0,0])==(167,50,60,255),result[0,0]
    priorities=np.array([0,1,2,3,4,4]);layers=np.zeros((16,16),dtype='uint8')
    effect=gpu_plane(packed,layers,priorities,1)
    surface=Surface((16,16));surface.draw(art,(0,0,16,16),alpha=True,foreground=effect)
    gpu=np.asarray(surface);difference=np.abs(gpu.astype('int16')-result[:,:,:3])
    assert difference.max()<=1,int(difference.max())
    # Native OBJ wins a BG priority tie; do not tint it with the BG behind it.
    tie=np.asarray(gpu_plane(packed,layers,priorities,0))
    assert np.all(tie[:,:,:3]==0) and np.all(tie[:,:,3]==16)
    from foreground_blend import eligibility
    from foreground_blend import begin_frame,eligibility_box
    energy=packed ^ np.uint64(8<<23) ^ np.uint64(16<<23)
    assert eligibility(energy,layers,priorities,0).all(),'Additive beam must cover an OBJ priority tie'
    assert not eligibility(energy,layers,priorities,0,0).any(),'Do not raise energy over a BG cut-in'
    owner_layers=np.full_like(layers,4)
    slow=eligibility(energy,owner_layers,priorities,0)
    assert slow.all(),'Native unit silhouette must receive the same beam'
    begin_frame(energy,priorities)
    assert np.array_equal(slow,eligibility(energy,owner_layers,priorities,0))
    assert eligibility_box(energy,(2,3,8,10),owner_layers[3:10,2:8],priorities,0).all()
    energy_effect=gpu_plane(energy,owner_layers,priorities,0)
    energy_surface=Surface((16,16));energy_surface.draw(art,(0,0,16,16),alpha=True,foreground=energy_effect)
    energy_cpu=np.asarray(blend_part(art,energy,slow,(1,0,0,0,1,0)))[:,:,:3]
    assert np.abs(np.asarray(energy_surface).astype('int16')-energy_cpu).max()<=1
    begin_frame(None,None)
    blocked=np.full((16,16),31|(1<<15)|(8<<18)|(8<<23)|(4<<32)|(1<<37),dtype='uint64')
    assert not eligibility(blocked,layers,priorities,2,2).any(),'Intervening BG1 must hide the BG2 cut-in'
    adjacent=blocked^(np.uint64(1<<37))^np.uint64(2<<37)
    assert eligibility(adjacent,layers,priorities,2,2).all()
    transparent=art.copy();transparent.putalpha(71)
    assert np.all(np.asarray(blend_part(transparent,packed,eligible,(1,0,0,0,1,0)))[:,:,3]==71)
    report=dict(color_arithmetic=True,priority_ties=True,additive_obj_ties=True,fast_slow_parity=True,additive_gpu_cpu_parity=True,intervening_opaque_layer_preserved=True,painted_alpha_preserved=True,gpu_cpu_max_difference=int(difference.max()))
    out=ROOT/'test_current/combat/foreground';out.mkdir(exist_ok=True)
    (out/'arithmetic_verification.json').write_text(json.dumps(report,indent=2));print(report)


if __name__=='__main__':main()
