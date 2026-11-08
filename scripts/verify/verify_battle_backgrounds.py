"""Replay actual battle saves through additional BG identification/composition."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_battle_backgrounds import BattleBackgroundRenderer
from gpu_surface import Surface

def main():
    out=ROOT/'test_current/battle_backgrounds';out.mkdir(exist_ok=True);core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves');renderer=BattleBackgroundRenderer(async_prepare=False);rows=[]
    try:
        for frame in (13110,13350,13620,13920,14850):
            core.load(ROOT/f'test_current/attract/battle_{frame}.state');core.run();native=core.native[:192];image=Image.fromarray(native).resize((960,720),Image.Resampling.NEAREST);start=time.perf_counter();matched=renderer.compose(image,native,core.ids,core.bg_layout);cold=(time.perf_counter()-start)*1000;image.save(out/f'battle_{frame}_hd.png');before=np.asarray(Image.fromarray(native).resize(image.size,Image.Resampling.NEAREST));after=np.asarray(image);changed=np.any(before!=after,2)
            allowed=np.zeros(core.ids.shape,dtype='bool')
            for layer,*_ in renderer.battle_layers(core.bg_layout):allowed|=core.ids==layer
            allowed=np.asarray(Image.fromarray(allowed.astype('uint8')*255).resize(image.size,Image.Resampling.NEAREST))>0
            assert not np.any(changed&~allowed),'foreground or HUD was overwritten'
            gpu=Surface.from_native(native,image.size);gpu_changed=renderer.compose(gpu,native,core.ids,core.bg_layout);gpu_pixels=np.asarray(gpu);difference=np.abs(gpu_pixels.astype('int16')-after.astype('int16'));gpu_max=int(difference.max());assert gpu_max<=3,(frame,gpu_max)
            gpu_times=[]
            for _ in range(10):
                surface=Surface.from_native(native,image.size);renderer.compose(surface,native,core.ids,core.bg_layout);gpu_times.append(renderer.last_ms)
            warm=[]
            for _ in range(10):renderer.compose(image,native,core.ids,core.bg_layout);warm.append(renderer.last_ms)
            rows.append(dict(frame=frame,matched=matched,identified=renderer.last_identification,painted=renderer.last_matches,cold_ms=cold,warm_ms=float(np.mean(warm)),changed_pixels=int(changed.sum()),gpu_max_error=gpu_max,gpu_plan_ms=float(np.mean(gpu_times)),bg_layout=core.bg_layout))
        core.load(ROOT/'test_current/formation/favorite_base.state');core.run();image=Image.fromarray(core.native[:192]).resize((960,720));start=time.perf_counter()
        for _ in range(50):assert not renderer.compose(image,core.native[:192],core.ids,core.bg_layout)
        negative=(time.perf_counter()-start)*1000/50
        report=dict(states=rows,menu_false_positive=False,menu_mean_ms=negative,errors={str(k):v for k,v in renderer.errors.items()});(out/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:core.close();renderer.close()

if __name__=='__main__':main()
