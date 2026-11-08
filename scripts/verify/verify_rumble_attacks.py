"""Replay native Eid firing and Bonta's attract attack, including HD parity."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
import numpy as np
from collections import Counter
from hd_core import Core,ROOT
from battle_rumble import BattleRumble

def main():
    results=[]
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/rumble_saves')
    for scene,frames in (('eid_firing',600),('bonta_attack',900)):
        variants=[];costs=[]
        for enabled in (False,True):
            c.enabled=enabled;c.api.retro_srw_set_hd_enabled(int(enabled))
            tracker=BattleRumble();events=[]
            try:
                c.load(ROOT/f'test_current/combat/{scene}.state')
                for frame in range(frames):
                    c.run();c.audio.clear();start=time.perf_counter();event=tracker.sample(c);costs.append((time.perf_counter()-start)*1000)
                    if event:events.append(dict(frame=frame,**event))
            finally:c.buttons=set()
            variants.append(events)
        assert variants[0]==variants[1],scene
        counts=Counter(e['reason'] for e in variants[1]);assert sum(counts.values())>0,scene
        results.append(dict(scene=scene,frames=frames,hd_parity=True,events=dict(counts),detector_median_ms=float(np.median(costs)),detector_p95_ms=float(np.percentile(costs,95)),timeline=variants[1]))
    c.close()
    (ROOT/'test_current/combat/rumble_attack_audit.json').write_text(json.dumps(results,indent=2));print(json.dumps([{k:v for k,v in r.items() if k!='timeline'} for r in results]))

if __name__=='__main__':main()
