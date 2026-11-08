"""Pixel and timing comparison of GPU composition against the established renderer."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
import numpy as np
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/performance';cpu=HDRenderer();gpu=HDRenderer(gpu_composition=True)
    assert gpu.gpu_composition,gpu.gpu_error
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'gpu_saves');rows=[]
    try:
        scenes=['formation/favorite_base.state','formation/formation.state','font/cutin_dialogue.state','scenario/final.state','map_icons/all_enemies_visible.state','localized_screens/chapter.state']
        scenes += [f'combat/{name}.state' for name in ('duo_cutin_full','quatre_cutin_full','duo_smile_cutin_full','sandrock_closeup_cutin_full','sandrock_weapons','duo_weapons') if (ROOT/f'test_current/combat/{name}.state').exists()]
        for state in scenes:
            c.load(ROOT/'test_current'/state);c.run();kw=dict(paused=True,parts=c.parts,obj=c.obj.raw,owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,backgrounds=c.backgrounds,bg_layout=c.bg_layout,sub_parts=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities))
            for screen in range(2):
                render=lambda r:r.render_top(c.native,c.ids,c.hd,**kw) if screen==0 else r.render_bottom(c.native,c.hd)
                a=np.asarray(render(cpu));b=np.asarray(render(gpu));delta=np.abs(a.astype('int16')-b.astype('int16'))
                stats=dict(scene=state,screen=screen,max_error=int(delta.max()),mean_error=float(delta.mean()),above_3=int(np.count_nonzero(delta>3)))
                if stats['max_error']>3:
                    from PIL import Image
                    Image.fromarray(a).save(out/'gpu_reference.png');Image.fromarray(b).save(out/'gpu_output.png')
                assert stats['max_error']<=3,stats
                times=[]
                for r in (cpu,gpu):
                    start=time.perf_counter()
                    for _ in range(10):np.asarray(render(r))
                    times.append((time.perf_counter()-start)*100)
                stats.update(cpu_ms=round(times[0],3),gpu_ms=round(times[1],3));rows.append(stats);print(json.dumps(stats),flush=True)
        (out/'gpu_surface_verification.json').write_text(json.dumps(rows,indent=2))
    finally:
        c.close()
        for r in (cpu,gpu):r.parts_renderer.close();r.backgrounds.close();r.scenario_backgrounds.close();r.map_icons.close()

if __name__=='__main__':main()
