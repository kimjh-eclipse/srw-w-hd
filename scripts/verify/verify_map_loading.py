"""Verify bounded visible-map preparation and exact baked icon colors."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
from pathlib import Path
import numpy as np
from PIL import Image
from hd_map_tiles import MapTilesRenderer,ROOT
from hd_map_icons import MapIconRenderer

def main():
    folder=ROOT/'graphics/map_tiles';spec=json.loads((folder/'library.json').read_text())['maps'][0]
    with Image.open(folder/spec['image']) as opened:art=opened.convert('RGB')
    worst=0;cases=0
    for screen in (768,832,960):
        size=(screen,screen*3//4);worldsize=(round(spec['width']*screen/256),round(spec['height']*screen/256));world=art.resize(worldsize,Image.Resampling.LANCZOS)
        for x,y in ((0,0),(17,33),(-9,-7),(world.width-100,world.height-200)):
            box=(x,y,x+size[0],y+size[1]);expected=np.asarray(world.crop(box));actual=np.asarray(MapTilesRenderer.resize_viewport(art,worldsize,box));difference=np.abs(expected.astype('int16')-actual.astype('int16'));worst=max(worst,int(difference.max()));assert difference.max()<=1;cases+=1
    icons=MapIconRenderer();assert icons.prepared_pixels is not None
    iconcases=0
    for resource in list(icons.records)[::9]:
        for palette in icons.palettes:
            for flip in (0,3):
                fast=icons.texture(resource,palette,flip,48).copy();pixels=icons.prepared_pixels;icons.prepared_pixels=None;icons.art.clear()
                try:slow=icons.texture(resource,palette,flip,48);assert np.array_equal(np.asarray(fast),np.asarray(slow)),(resource,palette,flip)
                finally:icons.prepared_pixels=pixels;icons.art.clear()
                iconcases+=1
    result=dict(viewport_cases=cases,viewport_max_channel_difference=worst,baked_icon_cases=iconcases,baked_icons_pixel_exact=True)
    native=np.asarray(Image.open(ROOT/'test_current/map_icons/menu_step_5_native.png').convert('RGB'))[192:384]
    sync=MapTilesRenderer();asynchronous=MapTilesRenderer(async_prepare=True);size=(768,576)
    try:
        expected=Image.fromarray(native).resize(size,Image.Resampling.NEAREST);assert sync.compose(expected,native)
        deadline=time.perf_counter()+15;loading=False
        while time.perf_counter()<deadline:
            actual=Image.fromarray(native).resize(size,Image.Resampling.NEAREST);asynchronous.compose(actual,native)
            loading|=any(row.get('loading',False) for row in asynchronous.last_matches)
            if asynchronous.last_matches and not asynchronous.pending:break
            time.sleep(.005)
        assert asynchronous.last_matches and not asynchronous.pending,'HD map preparation never completed'
        assert np.array_equal(np.asarray(expected),np.asarray(actual)),'settled HD terrain differs from synchronous rendering'
        asynchronous.prepare_errors['old']='stale';asynchronous.stamp=-1;asynchronous.checked=0;asynchronous.refresh()
        assert not asynchronous.prepare_errors and not asynchronous.art_cache and not asynchronous.world_views
        result.update(async_hd_completed=True,settled_map_pixel_exact=True,native_loading_fallback_observed=loading,refresh_invalidates_old_assets=True)
    finally:sync.close();asynchronous.close()
    (ROOT/'test_current/performance/map_loading_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':main()
