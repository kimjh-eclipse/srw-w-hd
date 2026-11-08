"""Audit archive coverage, exact face routing, frame positions and memory bounds."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,sys,time
import numpy as np
from PIL import Image,ImageDraw
from hd_portraits import PortraitRenderer
ROOT=PROJECT_ROOT;OUT=ROOT/'test_current/portrait';P=ROOT/'graphics/portraits'
def main():
    source=json.loads((P/'archive/catalog.json').read_text())['portraits'];library=json.loads((P/'library.json').read_text())['portraits'];known={x['name']:x['img'] for x in json.loads((P/'archive/observed_matches.json').read_text())}
    covered={x.get('archive_img',known.get(x['name'])) for x in library};missing=sorted({x['img'] for x in source}-covered)
    renderer=PortraitRenderer(async_prepare=False);hud=Image.open(ROOT/'test_current/robot/native_65040.png').convert('RGBA').crop((0,136,56,184));failures=[];count=0;start=time.perf_counter();visible=Image.new('L',(56,48));ImageDraw.Draw(visible).polygon([(4,1),(48,1),(52,5),(52,47),(4,47)],fill=255);visible=np.asarray(visible)>0
    for original in source:
        if original['img'] not in covered:continue
        rgba=Image.open(P/original['path']).convert('RGBA');panel=np.asarray(Image.alpha_composite(hud,rgba).convert('RGB'))
        for y in (0,24,136):
            native=np.zeros((384,256,3),dtype='uint8');native[y:y+48,:56]=panel;top=Image.fromarray(native[:192]).resize((1440,1080),Image.Resampling.NEAREST)
            if not renderer.compose(top,native):failures.append(dict(img=original['img'],y=y,error='not matched'));continue
            matched=next(x for x in library if x['name']==renderer.last_match);path=matched['portrait_mask'];other=np.asarray(Image.open(ROOT/'graphics'/path).convert('RGBA'));expected=np.asarray(rgba)
            mask=visible&((expected[:,:,3]>0)|(other[:,:,3]>0))
            if not np.array_equal((expected[:,:,:3]>>3)[mask],(other[:,:,:3]>>3)[mask]):failures.append(dict(img=original['img'],y=y,error='wrong variant',matched=renderer.last_match))
            if renderer.last_rectangle!=(0,y,56,48):failures.append(dict(img=original['img'],y=y,error='wrong coordinates'))
            count+=1
    result=dict(catalog_sources=len(source),covered_sources=len(covered),registered_items=len(library),missing=missing,checked_positions=count,failures=failures,texture_cache=len(renderer.cache),reference_cache=len(renderer.references),seconds=round(time.perf_counter()-start,2))
    (OUT/'catalog_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result));assert not failures
    return result
if __name__=='__main__':main()
