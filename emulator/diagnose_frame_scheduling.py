"""Headless video-cadence/snapshot-IPC measurements without production edits."""
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import pickle,time,json
from pathlib import Path
import numpy as np

def echo_snapshot(snapshot):return snapshot[4],time.perf_counter()

def summarize(samples):return dict(mean_ms=round(float(np.mean(samples)),4),p95_ms=round(float(np.percentile(samples,95)),4),max_ms=round(float(max(samples)),4))

def simulation(render_ms,core_ms=4,ipc_ms=1,seconds=10,gate=True):
    # Same ordering as player_worker: core tick, take, gated submit, <=2ms sleep.
    now=0.;next_frame=0.;last_draw=-100.;last_epoch=-1;epoch=0;future=None;draws=0;submitted=0
    while now<seconds*1000:
        if now>=next_frame:epoch+=1;next_frame+=1000/59.8261;now+=core_ms
        if future is not None and now>=future:future=None;draws+=1
        if future is None and epoch!=last_epoch and (not gate or now-last_draw>=1000/60):
            future=now+render_ms+ipc_ms;last_draw=now;last_epoch=epoch;submitted+=1
        now+=max(.03,min(2.,next_frame-now))
    return dict(render_ms=render_ms,core_ms=core_ms,ipc_ms=ipc_ms,rate_gate=gate,composition_fps=round(draws/seconds,2))

def main():
    from hd_core import Core,ROOT
    from frame_compositor import FrameCompositor
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/performance/scheduling_saves',frameskip=0)
    report={'frameskip':core.frameskip,'video_cadence':{}};probe=FrameCompositor.__new__(FrameCompositor);probe.dynamic_parts=core.dynamic_bridge;probe.render_width=960
    try:
        for name,path in [('ability','test_current/parts/result.state'),('battle','test_current/font/cutin_dialogue.state')]:
            core.load(ROOT/path,refresh_code=True);deltas=[];runs=[]
            for i in range(120):
                before=core.video_epoch;start=time.perf_counter();changed=core.run();runs.append((time.perf_counter()-start)*1000);core.audio.clear();deltas.append(core.video_epoch-before)
                assert changed==(deltas[-1]>0)
            report['video_cadence'][name]=dict(retro_runs=120,video_callbacks=sum(deltas),runs_without_video=deltas.count(0),callback_delta_counts={str(x):deltas.count(x) for x in set(deltas)},core_run=summarize(runs))
        snapshots=[];copies=[];serializes=[]
        for i in range(20):
            start=time.perf_counter();snapshot=probe.snapshot(core,False,i);copies.append((time.perf_counter()-start)*1000);snapshots.append(snapshot)
            start=time.perf_counter();encoded=pickle.dumps(snapshot,protocol=pickle.HIGHEST_PROTOCOL);serializes.append((time.perf_counter()-start)*1000)
        with ProcessPoolExecutor(max_workers=1,mp_context=mp.get_context('spawn')) as pool:
            pool.submit(echo_snapshot,snapshots[0]).result()
            roundtrips=[];child_delivery=[]
            for snapshot in snapshots:
                start=time.perf_counter();frame,child_time=pool.submit(echo_snapshot,snapshot).result();roundtrips.append((time.perf_counter()-start)*1000);child_delivery.append((child_time-start)*1000)
        report.update(snapshot_bytes=len(encoded),snapshot_copy=summarize(copies),pickle=summarize(serializes),pool_echo_roundtrip=summarize(roundtrips),pool_delivery_to_child=summarize(child_delivery))
    finally:core.close()
    report['scheduler_simulation']=[simulation(render,gate=gate) for render in (0,4,8,12,15,18,24) for gate in (True,False)]
    out=ROOT/'test_current/performance/frame_scheduling_diagnosis.json';out.write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':mp.freeze_support();main()
