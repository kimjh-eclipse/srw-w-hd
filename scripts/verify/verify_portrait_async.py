"""Check native fallback, GC-owned cleanup and real core progress during prep."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import gc,json,time,weakref,threading
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
import hd_portraits as portraits
from hd_core import Core
from scripts.diagnostics.profile_portraits import timing
ROOT=PROJECT_ROOT;OUT=ROOT/'test_current/portrait'
def main():
    native=np.zeros((192,256,3),dtype='uint8');native[136:184,:56]=np.asarray(Image.open(ROOT/'graphics/portraits/mao_native.png').convert('RGB'));surface=Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST)
    original=portraits._prepare_art
    def slow(item):time.sleep(.2);return original(item)
    with patch.object(portraits,'_prepare_art',slow):
        renderer=portraits.PortraitRenderer();before=np.asarray(surface).copy();start=time.perf_counter();drawn=renderer.compose(surface,native);fallback_ms=(time.perf_counter()-start)*1000
        assert not drawn and np.array_equal(before,np.asarray(surface))
    limit=time.perf_counter()+5
    while not renderer.compose(surface,native):assert time.perf_counter()<limit;time.sleep(.002)
    assert renderer.last_match=='mao' and np.any(before!=np.asarray(surface));assert len(renderer.pending)<=16
    reference=weakref.ref(renderer);del renderer;gc.collect();assert reference() is None
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=OUT/'performance_save')
    state=ROOT/'test_current/attract/target.state'
    def run(renderer=None):
        core.load(state);values=[];preparing_frames=0;assets=[p for p in renderer.items if p.get('archive_img')] if renderer else []
        for frame in range(240):
            if renderer:
                renderer.collect_prepared()
                if frame%5==0:renderer._art(assets[(frame//5)%len(assets)])
                preparing_frames+=bool(renderer.pending)
            start=time.perf_counter();core.run();core.audio.clear();values.append((time.perf_counter()-start)*1000)
        return timing(values),preparing_frames
    try:
        baseline,_=run();active=portraits.PortraitRenderer();background,frames=run(active)
        assert not active.prepare_errors and frames>0
        result=dict(native_fallback_preserved=True,fallback_call_ms=round(fallback_ms,3),ready_overlay=True,cleanup_without_close=True,core_without_portrait_prep=baseline,core_during_real_portrait_prep=background,frames_with_background_jobs=frames,queued_limit=16,prepare_errors=active.prepare_errors)
        ref=weakref.ref(active);del active;gc.collect();assert ref() is None
    finally:core.close()
    (OUT/'async_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
