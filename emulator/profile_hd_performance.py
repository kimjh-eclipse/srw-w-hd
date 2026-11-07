"""Measure native emulation vs HD preparation/composition on a fixed battle."""
import time,json,cProfile,pstats
from hd_core import Core,ROOT,HERE
from hd_renderer import HDRenderer
OUT=ROOT/'test_current/parts';OUT.mkdir(exist_ok=True)
def main():
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True);core.load(HERE/'demo.state',refresh_code=True)
    renderer=HDRenderer();inputs=json.loads((HERE/'demo_input.json').read_text());timings=[];profile=cProfile.Profile()
    for f in range(64700,65901):
        core.buttons={e['button'] for e in inputs if e['from']<=f<e['to']};t=time.perf_counter();core.run();core.audio.clear();native=time.perf_counter()-t
        if f%2:continue
        t=time.perf_counter();profile.enable()
        renderer.render_top(core.native,core.ids,core.hd,robot=core.robot,obj=core.obj.raw,parts=core.parts,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes)
        profile.disable();render=time.perf_counter()-t;timings.append(dict(frame=f,native_ms=native*1000,render_ms=render*1000,parts=int((core.parts[:,0]>0).sum())))
    core.close();profile.dump_stats(str(OUT/'performance.prof'))
    with (OUT/'performance_profile.txt').open('w') as stream:pstats.Stats(profile,stream=stream).sort_stats('cumulative').print_stats(22)
    result=dict(samples=len(timings),native_ms=sum(t['native_ms'] for t in timings)/len(timings),render_ms=sum(t['render_ms'] for t in timings)/len(timings),worst=sorted(timings,key=lambda t:t['render_ms'],reverse=True)[:12])
    (OUT/'performance.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
