"""Compare optimized local masks with the previous full-screen compositor."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import importlib.util,json
import numpy as np
from PIL import Image
from hd_core import Core,ROOT,HERE
from hd_parts import PartsRenderer
OUT=ROOT/'test_current/parts'
spec=importlib.util.spec_from_file_location('reference_compositor',OUT/'performance_reference.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
def main():
    r=PartsRenderer();core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True);core.load(HERE/'demo.state',refresh_code=True)
    inputs=json.loads((HERE/'demo_input.json').read_text());scenes={};wanted={65040,65220,65340,65390,65400,65520,65674,65680,65840,65880,66400,66580,67000,67080}
    try:
        for f in range(64700,67081):
            core.buttons={e['button'] for e in inputs if e['from']<=f<e['to']};core.run();core.audio.clear()
            if f not in wanted:continue
            before=Image.fromarray(core.native[:192]).resize((1440,1080),Image.Resampling.NEAREST);after=before.copy()
            args=(core.parts,core.obj.raw,core.ids,core.owners,core.bgpriors,core.bgparts,core.part_palettes)
            old.PartsRenderer.compose(r,before,*args);r.compose(after,*args)
            changed=int(np.any(np.asarray(before)!=np.asarray(after),axis=2).sum());scenes[f]=changed
            if changed:before.save(OUT/'optimization_reference.png');after.save(OUT/'optimization_actual.png')
            assert changed==0,(f,changed)
    finally:core.close()
    (OUT/'optimization_verification.json').write_text(json.dumps(dict(pixel_identical_scenes=scenes),indent=2));print(json.dumps(scenes))
if __name__=='__main__':main()
