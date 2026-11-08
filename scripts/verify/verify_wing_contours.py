"""Real Quatre/Deathscythe scenes plus silhouette/foreground invariants."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_renderer import HDRenderer
from painted_edges import cutin_visibility

def main():
    out=ROOT/'test_current/combat'
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'wing_saves')
    renderer=HDRenderer(gpu_composition=True);renderer.set_resolution(960);reports=[]
    try:
        for name in ('quatre_cutin_full','sandrock_closeup_cutin_full','sandrock_forecast','duo_map_forecast','duo_cutin_full'):
            core.load(out/(name+'.state'));core.refresh_video();core.audio.clear()
            kw=dict(parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout)
            image=renderer.render_top(core.native,core.ids,core.hd,paused=True,**kw)
            image.save(out/(name+'_contour_fixed.png'))
            if core.hd[0]>1:
                mask=np.asarray(cutin_visibility(core.ids,int(core.hd[5]),int(core.hd[6]),core.bgpriors,core.owners,core.obj.raw))
                # Farther BG must never trim a painted silhouette.
                back=(core.ids<4)&(core.bgpriors[np.minimum(core.ids,5)]>core.hd[6])
                assert np.all(mask[back]==255)
            reports.append(dict(scene=name,cutin=int(core.hd[0]),parts=int(np.count_nonzero(core.parts[:,0])),prepared=len(renderer.parts_renderer.prepared)))
        # Foreground OBJ and BG still occlude; the old source contour is not a gate.
        layers=np.full((192,256),2,dtype='uint8');layers[:20]=0;layers[20:40]=4
        attrs=np.zeros((128,4),dtype='<u2');owners=np.zeros_like(layers)
        mask=np.asarray(cutin_visibility(layers,1,1,[0,1,2,3,4,4],owners,attrs.tobytes()))
        assert not mask[:40].any() and np.all(mask[40:]==255)
        (out/'wing_contour_verification.json').write_text(json.dumps(reports,indent=2));print(reports,flush=True)
    finally:core.close();renderer.parts_renderer.close()

if __name__=='__main__':main()
