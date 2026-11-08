"""Verify same-screen multiple faces, changed top only, and four-face cost."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time,threading
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from hd_portraits import PortraitRenderer,ROOT
from scripts.diagnostics.profile_portraits import timing, memory
OUT=ROOT/'test_current/portrait';P=ROOT/'graphics/portraits'
def main():
    library=json.loads((P/'library.json').read_text())['portraits'];known={x['name']:x['img'] for x in json.loads((P/'archive/observed_matches.json').read_text())};byimg={p.get('archive_img',known.get(p['name'])):p for p in library}
    hud=Image.open(ROOT/'test_current/robot/native_65040.png').convert('RGBA').crop((0,136,56,184))
    panels={i:np.asarray(Image.alpha_composite(hud,Image.open(ROOT/'graphics'/p['portrait_mask']).convert('RGBA')).convert('RGB')) for i,p in byimg.items()}
    def frame(a,b,y=0):
        native=np.zeros((192,256,3),dtype='uint8');native[y:y+48,:56]=panels[a];native[136:184,:56]=panels[b];return native
    def check(renderer,native,top_id,bottom_id,y):
        canvas=Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST);before=np.asarray(canvas).copy()
        assert renderer.compose(canvas,native)
        assert set(renderer.last_rectangles)=={(0,y,56,48),(0,136,56,48)},(top_id,bottom_id,renderer.last_rectangles)
        assert len(renderer.last_matches)==2
        assert renderer.last_match==renderer.last_matches[0] and renderer.last_rectangle==renderer.last_rectangles[0]
        assert renderer.last_rectangle==(0,136,56,48)
        wanted={y:top_id,136:bottom_id}
        for name,rect in zip(renderer.last_matches,renderer.last_rectangles):
            found=next(p for p in library if p['name']==name);expected=byimg[wanted[rect[1]]]
            # Distinct source IDs may contain exactly identical visible faces.
            assert renderer._matches_reference(found,native,0,rect[1])
            assert renderer._matches_reference(expected,native,0,rect[1])
        changed=np.any(np.asarray(canvas)!=before,axis=2)
        for at in (y,136):assert changed[round(at*5.625):round((at+48)*5.625),:315].sum()>15000
        allowed=np.zeros(changed.shape,dtype=bool)
        for at in (y,136):allowed[round(at*5.625):round((at+48)*5.625),:315]=True
        assert not np.any(changed&~allowed)
        return canvas
    renderer=PortraitRenderer(async_prepare=False);ids=sorted(byimg);count=0;start=time.perf_counter()
    for n,i in enumerate(ids):
        j=ids[(n+137)%len(ids)];check(renderer,frame(i,j),i,j,0);count+=1
    # User's two-face layout, followed by changing only the top face.
    for y in (0,8,24):
        check(renderer,frame(1018,60,y),1018,60,y)
        result=check(renderer,frame(56,60,y),56,60,y)
        if y==8:result.save(OUT/'two_faces_duo_quatre_hd.png')
    reconstructed=check(renderer,frame(1018,60,8),1018,60,8);reconstructed.save(OUT/'two_faces_bless_quatre_hd.png')
    # A missing/returning top face must not leave a stale cached top overlay.
    native=frame(1018,60,8);native[:56]=0;surface=Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST);assert renderer.compose(surface,native);assert renderer.last_rectangles==[(0,136,56,48)]
    check(renderer,frame(56,60,8),56,60,8)
    catalog_seconds=time.perf_counter()-start
    native=frame(1018,60,8);surfaces=[Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST) for _ in range(2)];base_memory=memory();renderers=[PortraitRenderer(),PortraitRenderer()]
    original_open=Image.open;opens=[];main_thread=threading.get_ident()
    def tracked(*a,**kw):opens.append((str(a[0]),threading.get_ident()==main_thread));return original_open(*a,**kw)
    with patch('PIL.Image.open',tracked):
        start=time.perf_counter()
        for r,s in zip(renderers,surfaces):r.compose(s,native)
        cold_ms=(time.perf_counter()-start)*1000
        limit=time.perf_counter()+5
        while any(len(r.last_matches)!=2 for r in renderers):
            assert time.perf_counter()<limit
            for r,s in zip(renderers,surfaces):r.compose(s,native)
            time.sleep(.001)
    cold_main_opens=sum(x[1] for x in opens);opens.clear();values=[]
    with patch('PIL.Image.open',tracked):
        for _ in range(300):
            start=time.perf_counter()
            for r,s in zip(renderers,surfaces):assert r.compose(s,native) and len(r.last_matches)==2
            values.append((time.perf_counter()-start)*1000)
    result=dict(catalog_pair_cases=count,faces_checked=count*2,top_only_change=True,top_remove_return=True,overlap_positions_tested=[0,8,24],user_source_ids=dict(bless=1018,quatre=60,duo=56),catalog_seconds=round(catalog_seconds,2),two_screens_faces=4,cold_frame_ms=round(cold_ms,3),cold_main_image_opens=cold_main_opens,warm_four_faces=timing(values),warm_image_opens=len(opens),memory_before_two=base_memory,memory_after_two=memory(),cache_sizes=[len(r.cache) for r in renderers],note='Catalog cases reconstruct native frames from original assets; user live-scene replay is a separate check.')
    assert len(opens)==0 and cold_main_opens==0
    (OUT/'multiple_faces_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
