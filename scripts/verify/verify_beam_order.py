"""Same-frame energy ordering A/B. Continuous async replay is verified separately."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from hd_renderer import HDRenderer
import foreground_blend as blend

def main():
    out=ROOT/'test_current/combat/beam_order_comparison';out.mkdir(parents=True,exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    renderer=HDRenderer(gpu_composition=True);renderer.set_resolution(768)
    state=ROOT/'test_current/combat/named_attacks/unit_413/native_reference/diagnostic_preview/weapon_1613_capture/frame_1320.state'
    core.load(state);best=0;rows=[]
    try:
        for frame in range(90):
            core.run();core.audio.clear()
            kw=dict(paused=False,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout,cutin_layers=core.cutin_layers,effect_foreground=core.effect_foreground)
            blend.ENERGY_TIES=False
            before=renderer.render_top(core.native,core.ids,tuple(core.hd),**kw).to_pil().copy()
            blend.ENERGY_TIES=True
            after=renderer.render_top(core.native,core.ids,tuple(core.hd),**kw).to_pil().copy()
            a=np.asarray(before).astype('int16');b=np.asarray(after).astype('int16');diff=np.abs(a-b).max(2)
            assert not diff[384:].any(),'Beam ordering must not change the dialogue UI'
            count=int((diff>4).sum());tie=renderer.parts_renderer.last_stats.get('beam_tie_pixels',0)
            rows.append(dict(frame=frame,changed_pixels=count,energy_pixels=tie))
            if count>best and tie:
                best=count;before.save(out/'before.png');after.save(out/'after.png')
                Image.fromarray(np.minimum(diff*4,255).astype('uint8')).save(out/'difference.png')
                best_frame=frame
        report=dict(state=str(state.relative_to(ROOT)),frames=len(rows),best_changed_pixels=best,best_frame=locals().get('best_frame'),dialogue_unchanged=True,rows=rows,scope=__doc__)
        (out/'report.json').write_text(json.dumps(report,indent=2));print({k:v for k,v in report.items() if k!='rows'})
        assert best>0,'No visible energy ordering difference was reproduced'
    finally:
        blend.ENERGY_TIES=True;core.close();renderer.parts_renderer.close()
if __name__=='__main__':main()
