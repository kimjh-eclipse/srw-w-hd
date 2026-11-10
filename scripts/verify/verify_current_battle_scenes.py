"""Replay saved real-game battle scenes through the current core/compositor.

Reports sampled scenes, never substitutes them for full campaign coverage.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import argparse,json,time,ctypes as C
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core
from hd_renderer import HDRenderer

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--frames',type=int,default=180)
    parser.add_argument('--scenes',help='Comma-separated saved native scene names')
    args=parser.parse_args();out=ROOT/'test_current/combat/current_scenes';out.mkdir(exist_ok=True)
    scenes=['eid_firing','bonta_attack','vulcan','quatre_cutin_full','duo_cutin_full','getter_cutin','golion_cutin_full','sandrock_forecast','duo_map_forecast']
    if args.scenes:scenes=args.scenes.split(',')
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    renderer=HDRenderer(async_parts=True,dynamic_parts=True);renderer.set_resolution(768)
    rows=[];cards=[]
    try:
        for scene in scenes:
            c.load(ROOT/f'test_current/combat/{scene}.state')
            # Finish cold texture preparation while the diagnostic is paused.
            # A binding ID alone is not evidence of a displayed HD texture.
            c.run();c.audio.clear();deadline=time.monotonic()+30
            prefetch_groups=renderer.parts_renderer.prefetch_groups
            renderer.parts_renderer.prefetch_groups={}
            while True:
                renderer.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,
                    owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,
                    backgrounds=c.backgrounds,bg_layout=c.bg_layout,unknown=c.unknown_snapshot(),
                    sub_parts=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities))
                if not (renderer.parts_renderer.pending or renderer.parts_renderer.unmapped_pending):break
                if time.monotonic()>=deadline:
                    (out/'warmup_timeout.json').write_text(json.dumps(dict(scene=scene,pending=[renderer.parts_renderer.bindings[b-1] for b in renderer.parts_renderer.pending],unknown_pending=[dict(key=key,descriptor=entry[2],request=entry[1]) for key,entry in renderer.parts_renderer.unmapped_pending.items()],errors=renderer.parts_renderer.prepare_errors),indent=2))
                    raise AssertionError((scene,'HD preparation timed out'))
                time.sleep(.02)
            renderer.parts_renderer.prefetch_groups=prefetch_groups
            c.load(ROOT/f'test_current/combat/{scene}.state')
            seen=set();cutins=set();durations=[];active_frames=0
            c.api.retro_get_memory_data.restype=C.c_void_p;ram=c.api.retro_get_memory_data(2)
            for frame in range(args.frames):
                c.set_ready_parts(renderer.parts_renderer);c.run();c.audio.clear()
                active_frames+=int(C.c_uint32.from_address(ram+0xa6f38).value==128 and C.c_uint32.from_address(ram+0x1e7a10).value==0)
                if frame%6:continue
                start=time.perf_counter()
                image=renderer.render_top(c.native,c.ids,c.hd,paused=True,parts=c.parts,obj=c.obj.raw,
                    owners=c.owners,bgpriors=c.bgpriors,bgparts=c.bgparts,part_palettes=c.part_palettes,
                    backgrounds=c.backgrounds,bg_layout=c.bg_layout,unknown=c.unknown_snapshot(),
                    sub_parts=(c.sub_parts,c.sub_owners,c.sub_oam.raw,c.sub_palettes,c.sub_ids,c.sub_priorities))
                durations.append((time.perf_counter()-start)*1000)
                seen.update(int(x) for x in c.parts[:,0] if x)
                if c.hd[0]:cutins.add(int(c.hd[0]))
                if frame in (0,60,120):
                    image.save(out/f'{scene}_{frame}.png')
                    card=image.resize((384,288));ImageDraw.Draw(card).text((4,4),f'{scene} +{frame}',fill='yellow');cards.append(card)
            assert not renderer.parts_renderer.prepare_errors,renderer.parts_renderer.prepare_errors
            expected={'bonta_attack':75,'quatre_cutin_full':7,'duo_cutin_full':6,'getter_cutin':90,'golion_cutin_full':107}.get(scene)
            if expected is not None:
                assert expected in cutins,(scene,'HD cut-in was not recognized',sorted(cutins))
                assert expected in renderer.cutins.specs,(scene,'HD artwork not connected')
            if scene not in ('sandrock_forecast','duo_map_forecast'):
                assert active_frames>0,(scene,'fixture did not enter battle')
            rows.append(dict(scene=scene,native_game_frames=args.frames,active_battle_frames=active_frames,cutin_ids=sorted(cutins),observed_bindings=sorted(seen),
                renderer_errors=dict(renderer.parts_renderer.prepare_errors),compose_median_ms=float(np.median(durations)),
                all_weapons_verified=False))
            (out/'report.json').write_text(json.dumps(dict(scope='Saved native scenes, limited replay durations; not every weapon',scenes=rows),indent=2))
            print(scene,'bindings',len(seen),'cutins',sorted(cutins),flush=True)
        for page in range((len(cards)+8)//9):
            sheet=Image.new('RGB',(1152,864))
            for i,card in enumerate(cards[page*9:page*9+9]):sheet.paste(card,(i%3*384,i//3*288))
            sheet.save(out/f'contact_{page}.png')
    finally:c.close();renderer.parts_renderer.close()

if __name__=='__main__':main()
