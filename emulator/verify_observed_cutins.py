"""Replay native attract cut-ins and verify exact bridge IDs in game."""
import json
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    out=ROOT/'test_current/attract';core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True);renderer=HDRenderer(async_parts=True);results=[]
    try:
        for frame in range(8131):
            core.set_ready_parts(renderer.parts_renderer);core.run();core.audio.clear()
            if frame not in (7040,7080,8100,8130):continue
            expected=2 if frame<8000 else 3
            assert int(core.hd[0])==expected,(frame,list(core.hd))
            core.save(out/f'cutin_{expected}.state')
            image=renderer.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds)
            image.save(out/f'cutin_{frame}_hd.png');results.append(dict(frame=frame,id=int(core.hd[0])));print(results[-1],flush=True)
    finally:renderer.parts_renderer.close();core.close()
    (out/'cutin_verification.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
