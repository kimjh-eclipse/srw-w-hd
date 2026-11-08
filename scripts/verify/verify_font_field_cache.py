"""Compare per-field font caching to the previous full-canvas implementation."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import importlib.util,json,time
import numpy as np
from PIL import Image
from hd_fonts import FontRenderer,ROOT

def main():
    path=ROOT/'test_current/font/renderer_before_field_cache.py'
    spec=importlib.util.spec_from_file_location('previous_font',path);old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old);old.ROOT=ROOT
    reference=old.FontRenderer();current=FontRenderer();cases=[];timings={'previous':[],'fields':[]}
    for number in (0,1,3,4):
        source=np.asarray(Image.open(ROOT/f'test_current/font/scene_{number}.png').convert('RGB'))
        for screen in (0,1):cases.append((f'scene{number}_{screen}',source[screen*192:(screen+1)*192].copy(),False))
    ability=np.asarray(Image.open(ROOT/'test_current/font/scene_1.png').convert('RGB'))[:192].copy()
    digit=np.flatnonzero(np.array(current.compact_characters)=='7')[0]
    pixels=np.unpackbits(np.frombuffer(current.compact_keys[digit].tobytes(),dtype='uint8')).reshape(8,8).astype(bool)
    for frame in range(12):
        source=ability.copy();source[96:104,40:48]=0;source[96:104,40:48][pixels]=255
        source[120:148,160:240]=[frame*11,frame*3,80]
        if frame%3==0:source=source//2
        cases.append((f'digit_moving_background_{frame}',source,False))
    for i in range(5):
        source=cases[0][1].copy();source[120:]=np.clip(source[120:].astype('int16')-i*16,0,255).astype('uint8')
        cases.append((f'cutin_ink_{i}',source,True))
    for size in ((960,720),(1440,1080)):
        for name,source,only_text in cases:
            results=[]
            for label,renderer in [('previous',reference),('fields',current)]:
                target=Image.fromarray(source).resize(size,Image.Resampling.NEAREST)
                start=time.perf_counter();renderer.compose(target,source,only_text=only_text);timings[label].append((time.perf_counter()-start)*1000);results.append(np.asarray(target))
            assert np.array_equal(*results),(name,size,int(np.max(np.abs(results[0].astype('int16')-results[1].astype('int16')))))
    report=dict(pixel_exact_cases=len(cases)*2,mean_ms={k:round(float(np.mean(v)),3) for k,v in timings.items()},field_cache_entries=len(current.field_cache))
    (ROOT/'test_current/font/field_cache_verification.json').write_text(json.dumps(report,indent=2));print(report)

if __name__=='__main__':main()
