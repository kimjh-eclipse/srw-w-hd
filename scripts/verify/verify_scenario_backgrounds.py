"""Check installed scenario art against actual game frames and occluding UI."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_scenario_backgrounds import ScenarioBackgrounds

def main():
    out=ROOT/'test_current/scene_assets';renderer=ScenarioBackgrounds(async_prepare=False)
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves')
    report={}
    try:
        c.load(ROOT/'test_current/scenario/final.state');c.run()
        for screen in range(2):
            source=c.native[screen*192:(screen+1)*192];image=Image.fromarray(source).resize((1440,1080),Image.Resampling.NEAREST)
            before=np.asarray(image).copy();start=time.perf_counter();changed=renderer.compose(image,source)
            image.save(out/f'scenario_screen_{screen}_hd.png');match=renderer.last_match
            report[str(screen)]=dict(changed=changed,match=match,first_ms=(time.perf_counter()-start)*1000)
            if screen==1:
                assert changed and match['name']=='scenario_5390',report
                result=np.asarray(image);assert np.count_nonzero(np.any(result!=before,axis=2))>50000
        # Non-background scenes must not acquire unrelated room art.
        for state in ['font/grid.state','formation/formation.state']:
            c.load(ROOT/'test_current'/state);c.run()
            for source in [c.native[:192],c.native[192:]]:
                target=Image.fromarray(source).resize((1440,1080),Image.Resampling.NEAREST)
                assert not renderer.compose(target,source),(state,renderer.last_match)
        report['map_and_menu_false_positives']=0
        (out/'scenario_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:c.close();renderer.close()

if __name__=='__main__':main()
