"""Repeatable composition benchmark on the scripted demo.

Replays the built-in demo with its recorded input and composes every frame
the way the player does (asynchronous parts, runtime assembly, both screens,
GPU drawing without readback). Reports frame-time percentiles and exclusive
time per function, and can save sampled frames so two code versions can be
compared picture by picture.

Exclusive time means time spent in a function itself, not in what it calls,
so the rows can be added up.
"""
import argparse,cProfile,json,pstats,queue,sys,time
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core,HERE
from hd_renderer import HDRenderer


class Ready:
    ready_generation=-1;values=[]
    def __init__(self):self.dynamic_bindings=queue.SimpleQueue()
    def ready_bindings(self):return self.values


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--name',default='current');parser.add_argument('--start',type=int,default=64700);parser.add_argument('--frames',type=int,default=1800)
    parser.add_argument('--width',type=int,default=768);parser.add_argument('--sample',type=int,default=90,help='save every Nth frame for picture comparison')
    parser.add_argument('--compare',help='name of an earlier run to compare sampled frames against');parser.add_argument('--no-profile',action='store_true');parser.add_argument('--stage-window',type=int,nargs=2,default=None,help='only time stages for frame offsets in [a,b)');parser.add_argument('--stages',action='store_true',help='wall-clock time per stage without the profiler (stages nest; do not add them up)')
    args=parser.parse_args()
    out=ROOT/'test_current/performance/demo_benchmark'/args.name;out.mkdir(parents=True,exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/performance/demo_benchmark/isolated_saves')
    renderer=HDRenderer(async_parts=True,dynamic_parts=core.dynamic_bridge,gpu_composition=True);renderer.set_resolution(args.width);parts=renderer.parts_renderer
    from gpu_surface import backend
    gpu=backend();ready=Ready();events=json.loads((HERE/'demo_input.json').read_text());core.load(HERE/'demo.state',refresh_code=True)
    times=[];samples={};profile=None if args.no_profile or args.stages else cProfile.Profile()
    stage_ms={};stage_calls={}
    def watch(owner,method,label):
        original=getattr(owner,method,None)
        if original is None:return
        def timed(*a,**k):
            begun=time.perf_counter()
            try:return original(*a,**k)
            finally:
                if watch.on:stage_ms[label]=stage_ms.get(label,0)+(time.perf_counter()-begun)*1000;stage_calls[label]=stage_calls.get(label,0)+1
        setattr(owner,method,timed)
    watch.on=False
    if args.stages:
        text=renderer.text_renderer
        for owner,method,label in [(text,'_recognize','text._recognize'),(text,'recognize','text.recognize'),(text,'clean_native','text.clean_native'),(text,'_heal_native','text._heal_native'),(text,'compose','text.compose'),
            (renderer.bottom_text_renderer,'compose','bottom_text.compose'),(renderer.menu_scene,'identify','menu.identify'),(renderer.menu_scene,'compose','menu.compose'),
            (renderer.battle_backgrounds,'compose','battle_bg.compose'),(renderer.battle_backgrounds,'identify','battle_bg.identify'),(renderer.backgrounds,'compose','bg.compose'),(renderer.scenario_backgrounds,'compose','scenario_bg.compose'),
            (renderer.map_tiles,'compose','map_tiles.compose'),(renderer.map_tiles,'phase','map_tiles.phase'),(renderer.map_icons,'compose','map_icons.compose'),
            (parts,'compose','parts.compose'),(parts,'sprite','parts.sprite'),(parts,'prefetch_related','parts.prefetch_related'),(parts,'schedule_unknown','parts.schedule_unknown'),(parts,'collect_prepared','parts.collect_prepared'),(parts,'rescue','parts.rescue'),
            (renderer.portraits,'compose','portraits.compose'),(renderer.ui_labels,'compose','ui_labels.compose'),(renderer.localized_screens,'compose','localized.compose'),(renderer.localized_screens,'stage_key','localized.stage_key'),
            (renderer,'render_top','render_top'),(renderer,'render_bottom','render_bottom'),(gpu,'render','gpu.render'),(gpu.ctx,'finish','gpu.finish')]:watch(owner,method,label)
        import foreground_blend
        for name in ('gpu_plane','eligibility','active'):watch(foreground_blend,name,'foreground.'+name)
    def compose():
        sub=(core.sub_parts,core.sub_owners,core.sub_oam.raw,core.sub_palettes,core.sub_ids,core.sub_priorities) if core.sub_bridge else None
        top=renderer.render_top(core.native,core.ids,tuple(core.hd),paused=False,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,
            part_palettes=core.part_palettes,backgrounds=core.backgrounds,unknown=core.unknown_snapshot(),bg_layout=core.bg_layout,sub_parts=sub,cutin_layers=core.cutin_layers,effect_foreground=core.effect_foreground)
        bottom=renderer.render_bottom(core.native,tuple(core.hd))
        gpu.render(top,components=4,draw_only=True)
        if bottom is not compose.last_bottom:gpu.render(bottom,components=4,draw_only=True);compose.last_bottom=bottom
        gpu.ctx.finish();return top,bottom
    compose.last_bottom=None
    try:
        for frame in range(args.start,args.start+args.frames):
            core.buttons={e['button'] for e in events if e['from']<=frame<e['to']}
            if ready.ready_generation!=parts.ready_generation:ready.ready_generation=parts.ready_generation;ready.values=parts.ready_bindings()
            while True:
                try:ready.dynamic_bindings.put(parts.dynamic_bindings.get_nowait())
                except queue.Empty:break
            core.set_ready_parts(ready);core.run();core.audio.clear()
            warm=frame-args.start>=120   # the first two seconds load the catalogue and the texture process
            inside=warm and (args.stage_window is None or args.stage_window[0]<=frame-args.start<args.stage_window[1])
            if profile is not None and inside:profile.enable();main.profiled=getattr(main,'profiled',0)+1
            watch.on=warm and (args.stage_window is None or args.stage_window[0]<=frame-args.start<args.stage_window[1]);counted=getattr(main,'counted',0)+int(watch.on);main.counted=counted;started=time.perf_counter();top,bottom=compose();elapsed=(time.perf_counter()-started)*1000;watch.on=False
            if profile is not None and inside:profile.disable()
            if warm:times.append(elapsed)
            if args.sample and (frame-args.start)%args.sample==0 and warm:
                samples[frame]=np.concatenate([np.asarray(top),np.asarray(bottom)],axis=1)
    finally:core.close();parts.close()
    ordered=sorted(times);pick=lambda q:round(ordered[min(len(ordered)-1,int(len(ordered)*q))],2)
    report=dict(name=args.name,frames=len(times),width=args.width,ms=dict(mean=round(sum(times)/len(times),2),p50=pick(.5),p95=pick(.95),p99=pick(.99),max=round(ordered[-1],2)),
        over_16_7ms=round(sum(t>16.7 for t in times)/len(times),3))
    if stage_ms:report['stage_ms_per_frame']={k:[round(v/max(1,main.counted),3),round(stage_calls[k]/max(1,main.counted),2)] for k,v in sorted(stage_ms.items(),key=lambda item:-item[1])}
    bins=[times[i:i+120] for i in range(0,len(times),120)];report['mean_ms_by_2s']=[round(sum(b)/len(b),1) for b in bins]
    np.savez_compressed(out/'samples.npz',**{str(k):v for k,v in samples.items()})
    if profile is not None:
        stats=pstats.Stats(profile);rows=[]
        for (file,line,name),(calls,_,own,total,_) in stats.stats.items():
            rows.append(dict(function=f'{Path(file).name}:{name}' if file not in ('~',) else name,calls=calls,exclusive_ms_per_frame=round(own*1000/main.profiled,3),inclusive_ms_per_frame=round(total*1000/main.profiled,3)))
        rows.sort(key=lambda r:-r['exclusive_ms_per_frame']);report['exclusive']=rows[:45]
        modules={}
        for row in rows:modules[row['function'].split(':')[0]]=modules.get(row['function'].split(':')[0],0)+row['exclusive_ms_per_frame']
        report['exclusive_by_module']={k:round(v,2) for k,v in sorted(modules.items(),key=lambda item:-item[1])[:20]}
    if args.compare:
        other=np.load(ROOT/'test_current/performance/demo_benchmark'/args.compare/'samples.npz');diffs=[]
        for key,picture in samples.items():
            if str(key) not in other.files or other[str(key)].shape!=picture.shape:continue
            delta=np.abs(picture.astype('int16')-other[str(key)].astype('int16'));diffs.append(dict(frame=key,differing_pixels=int((delta.max(2)>0).sum()),max=int(delta.max()),mean=round(float(delta.mean()),4)))
        report['compared_with']=args.compare;report['picture_differences']=diffs
        report['identical_frames']=sum(1 for d in diffs if d['differing_pixels']==0);report['compared_frames']=len(diffs)
    (out/'report.json').write_text(json.dumps(report,indent=1),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('exclusive','picture_differences')},indent=1))
    for row in report.get('exclusive',[])[:28]:print(f"{row['exclusive_ms_per_frame']:7.3f} ms  {row['calls']:7d} calls  {row['function']}")
    for d in report.get('picture_differences',[]):
        if d['differing_pixels']:print('differs',d)


if __name__=='__main__':main()
