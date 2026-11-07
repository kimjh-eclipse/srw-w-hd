"""Real twelve-scene GPU equivalence and independent persistent PBO timings."""
import json,time,csv
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_renderer import HDRenderer
from gpu_surface import backend
from persistent_pbo_prototype import PersistentPBO,production_draw_only

OUT=ROOT/'test_current/performance'

def main():
    renderer=HDRenderer(async_parts=False,gpu_composition=True);assert renderer.gpu_composition,renderer.gpu_error
    renderer.set_resolution(960);gpu=backend();persistent=PersistentPBO();draw=production_draw_only(gpu)
    report=dict(renderer=gpu.ctx.info.get('GL_RENDERER'),version=gpu.ctx.version_code,arb_buffer_storage='GL_ARB_buffer_storage' in gpu.ctx.extensions,actual_cases=[]);references={};csv_rows=[]
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=OUT/'persistent_saves')
    scenes=['formation/favorite_base.state','formation/formation.state','font/cutin_dialogue.state','scenario/final.state','map_icons/all_enemies_visible.state','localized_screens/chapter.state']
    try:
        for number,state in enumerate(scenes):
            core.load(ROOT/'test_current'/state,refresh_code=True);core.run()
            kwargs=dict(parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,bg_layout=core.bg_layout)
            for screen in (0,1):
                surface=renderer.render_top(core.native,core.ids,core.hd,**kwargs) if screen==0 else renderer.render_bottom(core.native,core.hd)
                assert hasattr(surface,'rgba_pipeline')
                tag=(state,screen);reference=gpu.render(surface,components=4);references[tag]=reference
                pixels,returned=persistent.read(surface.size,tag,lambda:draw(surface))
                assert np.array_equal(pixels,references[returned]),(tag,returned,'persistent pixels differ')
                report['actual_cases'].append(dict(scene=state,screen=screen,returned=list(returned),pixel_exact=True,operations=len(surface.ops)))
        pixels,returned=persistent.read(surface.size,('drain',),lambda:draw(surface))
        assert np.array_equal(pixels,references[returned])
        report['actual_cases'].append(dict(drain=True,returned=list(returned),pixel_exact=True))
        assert {tuple(row['returned']) for row in report['actual_cases']}==set(references)
        # Explicit size transitions and pause/reset with different moving scenes.
        from verify_rgba_transport import scene
        expected={};persistent.reset()
        for frame in range(12):
            size=(960,720) if frame<4 or frame>=8 else (1440,1080)
            surface,pixels=scene(frame,size);expected[frame]=pixels
            actual,returned=persistent.read(size,frame,lambda:draw(surface))
            assert np.array_equal(actual,expected[returned]),('moving/size',frame,returned)
        persistent.reset();surface,pixels=scene(30,(960,720));actual,tag=persistent.read(surface.size,30,lambda:draw(surface))
        assert tag==30 and np.array_equal(actual,pixels)
        report['resolution_and_paused_reset_exact']=True
        # Same draw commands, native pixels and tags for each readback strategy.
        for size in ((960,720),(1440,1080)):
            surface,_=scene(52,size)
            for mode in ('standard_pbo','persistent_coherent'):
                persistent.reset();gpu.reset_pipeline()
                for iteration in range(42):
                    start=time.perf_counter()
                    if mode=='standard_pbo':pixels,tag=gpu.render(surface,components=4,pipeline_tag=iteration)
                    else:pixels,tag=persistent.read(size,iteration,lambda:draw(surface))
                    elapsed=(time.perf_counter()-start)*1000
                    if iteration>=8:csv_rows.append(dict(mode=mode,width=size[0],iteration=iteration,returned_tag=tag,total_ms=round(elapsed,5)))
            report[str(size[0])]={mode:dict(mean_ms=round(float(np.mean([x['total_ms'] for x in csv_rows if x['mode']==mode and x['width']==size[0]])),4),p95_ms=round(float(np.percentile([x['total_ms'] for x in csv_rows if x['mode']==mode and x['width']==size[0]],95)),4)) for mode in ('standard_pbo','persistent_coherent')}
        report['persistent_internal_mean_ms']={key:round(float(np.mean([x[key] for x in persistent.metrics[-34:]])),4) for key in ('wait_ms','copy_ms')}
        assert persistent.gl.error()==0
    finally:
        persistent.close();core.close();renderer.parts_renderer.close();renderer.backgrounds.close();renderer.scenario_backgrounds.close();renderer.map_icons.close()
        if hasattr(renderer,'battle_backgrounds'):renderer.battle_backgrounds.close()
    with (OUT/'persistent_pbo_frames.csv').open('w',newline='',encoding='utf-8') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(csv_rows[0]));writer.writeheader();writer.writerows(csv_rows)
    (OUT/'persistent_pbo_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
