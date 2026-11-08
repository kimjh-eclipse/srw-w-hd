"""Compare the same active replay frames, excluding boot and initial loading."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
from pathlib import Path
import numpy as np

ROOT=PROJECT_ROOT
FOLDER=ROOT/'test_current/performance'

def summarize(label):
    result={};trace=FOLDER/f'hitch_{label}_render.json';ui=FOLDER/f'hitch_{label}_ui.json'
    active=lambda r:65400<r.get('frame',r.get('emulated_frame',0))<67500
    if trace.exists():
        data=json.loads(trace.read_text());rows=[r for r in (data if isinstance(data,list) else data['frames']) if active(r)]
        costs=np.array([r['ms'] for r in rows]);result['render_ms']=dict(zip(('median','p95','p99','max'),np.percentile(costs,[50,95,99,100]).round(3)))
        result['cold_map_frame_ms']=next((round(r['ms'],3) for r in rows if r['frame']==67144),None)
        result['first_menu_frame_ms']=max((round(r['ms'],3) for r in rows if 67160<=r['frame']<=67166),default=None)
    if ui.exists():
        data=json.loads(ui.read_text());rows=[r for r in data['presents'] if active(r)];costs=np.array([r['interval_ms'] for r in rows])
        result['presentation_interval_ms']=dict(zip(('median','p95','p99','max'),np.percentile(costs,[50,95,99,100]).round(3)))
        result['gaps_over_33ms']=int((costs>33).sum());result['gaps_over_50ms']=int((costs>50).sum())
    path=FOLDER/f'live_hitch_{label}_metrics.json'
    if path.exists():
        rows=[r for r in json.loads(path.read_text())['history'] if active(r)]
        result.update(one_second_samples=len(rows),display_fps_mean=round(float(np.mean([r['display_fps'] for r in rows])),3),display_fps_one_second_low=min(r['display_fps'] for r in rows),native_fps_mean=round(float(np.mean([r['emulation_fps'] for r in rows])),3))
    return result

if __name__=='__main__':
    result=dict(native_target_hz=59.8261,active_replay_frames=[65401,67499],internal_width=768,method='Same saved battle replay in the foreground; no concurrent CPU tests. One-second windows include scene transitions. Frame traces are diagnostic, control playback omits traces.',runs={label:summarize(label) for label in ('before','final','control','repeat')},locked_native_rate=False)
    (FOLDER/'hitch_comparison.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
