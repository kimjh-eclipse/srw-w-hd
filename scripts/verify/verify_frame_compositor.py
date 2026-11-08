"""Measure actual worker game speed while HD scene composition is active."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
from hd_core import ROOT
from scripts.verify.verify_player import Session

def main():
    results=[]
    for scene,frame in [('target',8910),('battle_13620',13620)]:
        session=Session(state=ROOT/f'test_current/attract/{scene}.state',state_frame=frame)
        try:
            session.until('loaded');session.until('frame');session.send('pause',value=False);session.until('paused')
            start=time.perf_counter();statuses=[];frames=0
            while time.perf_counter()-start<4.2:
                if not session.pipe.poll(.02):continue
                message=session.pipe.recv()
                assert message['event']!='error',message
                if message['event']=='status':statuses.append((time.perf_counter(),message['frame']))
                if message['event']=='frame':frames+=1
            assert len(statuses)>=3,statuses
            statuses=statuses[1:] if len(statuses)>3 else statuses
            fps=(statuses[-1][1]-statuses[0][1])/(statuses[-1][0]-statuses[0][0]);result=dict(scene=scene,emulated_fps=round(fps,2),display_frames=frames,seconds=round(time.perf_counter()-start,2));results.append(result);print(result,flush=True)
            assert fps>54,result
        finally:session.close()
    (ROOT/'test_current/parts/worker_speed.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
