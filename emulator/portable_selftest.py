"""Exercise the actual frozen process graph with optional external private fixtures."""
import argparse,json,time,sys,os
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('--self-test',type=Path,required=True);p.add_argument('--rom',type=Path);p.add_argument('--state',type=Path);args=p.parse_args()
    import numpy as np
    from runtime_paths import data_dir,FROZEN
    from hd_fonts import FontRenderer
    from pad_process import PadClient
    result=dict(frozen=FROZEN,python_executable=sys.executable,python_environment_required=False,font_table_entries=len(FontRenderer().keys),data_dir=str(data_dir()))
    pad=PadClient()
    try:
        deadline=time.monotonic()+3
        while time.monotonic()<deadline:
            pad.poll()
            if pad.last_update>pad.started and pad.process and pad.process.is_alive():break
            time.sleep(.02)
        assert pad.process and pad.process.is_alive(),'Controller worker did not start'
        assert pad.last_update>pad.started,'Controller worker did not respond'
        result.update(controller_process=True,connected_controllers=len(pad.devices()))
    finally:pad.close()
    # Finished part textures delivered with the release: found by key without registration work.
    from hd_parts import PartsRenderer
    parts=PartsRenderer(async_prepare=False);parts.load_baked()
    active=[b for b,s in enumerate(parts.bindings,1) if not (s.get('source_binding') or s.get('runtime_texture') or s.get('disabled') or b in parts.quarantine)]
    sample=[b for b in active if b in parts.baked][::997]
    for b in sample:
        image,_=parts.disk_cache.get(parts.texture_key(b,parts.bindings[b-1]['w'],parts.bindings[b-1]['h']));assert image.size[0]>0
    result.update(shipped_store=str(parts.disk_cache.shipped_path),player_store=str(parts.disk_cache.path),active_parts=len(active),baked_parts=sum(b in parts.baked for b in active),baked_sample_read=len(sample),
        player_store_rows=parts.disk_cache.db().execute('SELECT count(*) FROM textures').fetchone()[0])
    parts.disk_cache.close()
    if args.rom:
        from hd_core import Core,ROOT
        from frame_compositor import FrameCompositor
        c=Core(args.rom,demo=False,user_dir=data_dir()/'selftest_saves');renderer=FrameCompositor(async_parts=True,dynamic_parts=True)
        try:
            if args.state:c.load(args.state)
            c.refresh_video();c.audio.clear();start=time.monotonic()
            while True:
                image=renderer.capture(c,True)
                if not renderer.needs_refresh or time.monotonic()-start>40:break
                c.set_ready_parts(renderer.ready)
                if args.state:c.load(args.state)
                c.refresh_video();c.audio.clear();time.sleep(.05)
            pixels=np.asarray(image);assert pixels.max()>0 and pixels.std()>10,'Empty game frame'
            image.save(args.self_test.with_suffix('.png'))
            result.update(native_core=True,hd_frame_size=list(image.size),frame_worker=True,prepared_parts=len(renderer.ready.values),hd_cutin_id=int(c.hd[0]))
            result['native_energy_feedback_bridge']=hasattr(c.api,'retro_srw_copy_effect_debug')
            assert result['native_energy_feedback_bridge'],'Updated energy-feedback bridge missing'
            result['native_multilayer_cutin_bridge']=c.layer_cutin_bridge
            result['active_cutin_layers']=c.cutin_layers.tolist()
            assert result['native_multilayer_cutin_bridge'],'Simultaneous pilot cut-in bridge missing'
            if args.state and args.state.stem=='quatre_cutin_full':assert c.hd[0]==7,'Quatre cut-in was not registered in the frozen core'
        finally:renderer.close();c.close()
    args.self_test.parent.mkdir(parents=True,exist_ok=True);args.self_test.write_text(json.dumps(result,indent=2),encoding='utf-8')

if __name__=='__main__':main()
