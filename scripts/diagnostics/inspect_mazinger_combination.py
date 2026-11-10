"""Capture exact FDS beam/robot parts and native references from an isolated state."""
import argparse,json,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from hd_renderer import HDRenderer
from scripts.diagnostics import inspect_attract_resources as capture

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--saved-states',action='store_true');args=parser.parse_args()
    folder=ROOT/'test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture'
    out=ROOT/'test_current/combat/mazinger_combination';out.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'isolated_saves')
    renderer=HDRenderer(async_parts=True,dynamic_parts=True);renderer.set_resolution(768)
    def paint():
        return renderer.render_top(core.native,core.ids,core.hd,paused=True,parts=core.parts,obj=core.obj.raw,
            owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,
            backgrounds=core.backgrounds,bg_layout=core.bg_layout,unknown=core.unknown_snapshot(),cutin_layers=core.cutin_layers)
    try:
        capture.OUT=out
        if args.saved_states:
            for frame in (1400,1560,1800,1920):
                state=out/f'frame_{frame}.state';core.load(state);core.set_ready_parts(renderer.parts_renderer);core.run();core.audio.clear()
                deadline=time.monotonic()+30
                while time.monotonic()<deadline:
                    paint();renderer.parts_renderer.collect_prepared()
                    visible={int(row[0]) for row in core.parts if row[0]}
                    if all(renderer.parts_renderer.bindings[i-1].get('source_binding',i) in renderer.parts_renderer.prepared for i in visible):break
                    time.sleep(.02)
                core.load(state);core.set_ready_parts(renderer.parts_renderer);core.run();core.audio.clear()
                paint().save(out/f'hd_{frame}.png');capture.snapshot(core,frame)
                identifiers={int(row[0]) for row in core.parts if row[0]}
                record=dict(parts=core.parts.tolist(),cutins=core.cutin_layers.tolist(),bindings={str(i):renderer.parts_renderer.bindings[i-1] for i in identifiers},
                    unprepared_bindings=[i for i in identifiers if renderer.parts_renderer.bindings[i-1].get('source_binding',i) not in renderer.parts_renderer.prepared])
                (out/f'parts_{frame}.json').write_text(json.dumps(record,indent=2));print('captured saved state',frame,flush=True)
            return
        for replay in range(2):
            core.load(folder/'frame_1320.state')
            for frame in range(1321,1981):
                core.buttons=set();core.set_ready_parts(renderer.parts_renderer);core.run();core.audio.clear()
                if frame%12==0:paint()
                if frame not in (1400,1560,1800,1920):continue
                if replay==0:continue
                # A paused capture must prove prepared textures, rather than
                # photograph a temporary native fallback during lazy loading.
                deadline=time.monotonic()+30
                while time.monotonic()<deadline:
                    paint();renderer.parts_renderer.collect_prepared()
                    visible={int(row[0]) for row in core.parts if row[0]}
                    sources={renderer.parts_renderer.bindings[i-1].get('source_binding',i) for i in visible}
                    if sources.issubset(set(renderer.parts_renderer.prepared)):break
                    time.sleep(.02)
                image=paint();capture.snapshot(core,frame);core.save(out/f'frame_{frame}.state');image.save(out/f'hd_{frame}.png')
                identifiers={int(row[0]) for row in core.parts if row[0]}
                record=dict(parts=core.parts.tolist(),bgparts=[row.tolist() for row in core.bgparts if row[0]],
                    cutins=core.cutin_layers.tolist(),bindings={str(i):renderer.parts_renderer.bindings[i-1] for i in identifiers},
                    registration_stats={str(i):renderer.parts_renderer.registration_stats.get(i) for i in identifiers})
                record['unprepared_bindings']=[i for i in identifiers if renderer.parts_renderer.bindings[i-1].get('source_binding',i) not in renderer.parts_renderer.prepared]
                (out/f'parts_{frame}.json').write_text(json.dumps(record,indent=2));print('captured',frame,flush=True)
        core.set_hd(False)
        from PIL import Image
        for frame in (1400,1560,1800,1920):
            core.load(out/f'frame_{frame}.state');core.run();core.audio.clear()
            Image.fromarray(core.native[:192]).save(out/f'original_{frame}.png')
        print('finished native replay',flush=True)
    finally:core.close();renderer.parts_renderer.close()

if __name__=='__main__':main()
