"""Pixel-for-pixel comparison with the pre-optimization compositors."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ast
import importlib.util
import json
import time
import numpy as np
from PIL import Image
import hd_parts
from hd_core import Core, ROOT
from hd_backgrounds import BackgroundRenderer


def main():
    out=ROOT/'test_current/performance'
    spec=importlib.util.spec_from_file_location('background_reference',out/'background_reference.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.ROOT=ROOT
    reference=module.BackgroundRenderer();fast=BackgroundRenderer();rng=np.random.default_rng(71)
    timings=[];cases=0
    for bid in (1,3,4):
        for x,y in ((0,0),(31,19),(255,129)):
            art,source=reference._art(bid);height,width=source.shape[:2]
            fast._art(bid)
            for shape in ('full','actors','text'):
                ids=np.full((192,256),3,dtype='uint8')
                if shape=='actors':ids[30:100,35:90]=4;ids[10:75,170:250]=4
                if shape=='text':ids[128:]=0;ids[50:120,70:130]=4
                native=source[(np.arange(192)+y)%height][:,(np.arange(256)+x)%width].copy()
                native[ids!=3]=[12,20,27]
                base=Image.fromarray(rng.integers(0,256,(192,256,3),dtype='uint8')).resize((1440,1080),Image.Resampling.NEAREST)
                before=base.copy();after=base.copy();row=[(bid,x,y,3)]
                start=time.perf_counter();reference.compose(before,native,ids,row);slow_ms=(time.perf_counter()-start)*1000
                start=time.perf_counter();fast.compose(after,native,ids,row);fast_ms=(time.perf_counter()-start)*1000
                assert before.tobytes()==after.tobytes(),(bid,x,y,shape)
                timings.append((slow_ms,fast_ms));cases+=1
    tree=ast.parse((out/'parts_reference.py').read_text(encoding='utf8'))
    cls=next(node for node in tree.body if isinstance(node,ast.ClassDef) and node.name=='PartsRenderer')
    function=next(node for node in cls.body if isinstance(node,ast.FunctionDef) and node.name=='compose')
    function.name='reference_compose';namespace=dict(hd_parts.__dict__)
    exec(compile(ast.Module(body=[function],type_ignores=[]),'reference_compose','exec'),namespace)
    parts=hd_parts.PartsRenderer();core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves')
    try:
        for state in ('parts/result.state','font/cutin_dialogue.state','attract/target.state','formation/formation.state'):
            core.load(ROOT/'test_current'/state);core.run()
            args=(core.parts,core.obj.raw,core.ids,core.owners,core.bgpriors,core.bgparts,core.part_palettes)
            before=Image.fromarray(core.native[:192]).resize((1440,1080),Image.Resampling.NEAREST);after=before.copy()
            namespace['reference_compose'](parts,before,*args)
            parts.compose(after,*args)
            assert before.tobytes()==after.tobytes(),state
    finally:core.close();parts.close()
    report=dict(background_pixel_identical_cases=cases,parts_pixel_identical_scenes=4,
                background_reference_ms=float(np.mean([a for a,b in timings])),
                background_optimized_ms=float(np.mean([b for a,b in timings])))
    (out/'compositor_fast_paths.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))


if __name__=='__main__':main()
