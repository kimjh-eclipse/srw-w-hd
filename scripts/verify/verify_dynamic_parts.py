"""Force an actual ROM rectangle through exact tile assembly and native readiness."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json,time
import numpy as np
from hd_core import Core,ROOT
from hd_renderer import HDRenderer
from tile_compositor import TileCompositor

def main():
    out=ROOT/'test_current/parts';state=ROOT/'test_current/attract/target.state'
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'dynamic_saves');r=HDRenderer(async_parts=True,dynamic_parts=True)
    try:
        assert core.dynamic_bridge,'new native assembly bridge missing'
        dummy=(C.c_uint*1)(0);core.api.retro_srw_register_parts(dummy,0);core.api.retro_srw_register_indexed_parts(dummy,dummy,0)
        core.load(state);core.set_ready_parts(r.parts_renderer);core.run();snapshot=core.unknown_snapshot();assert snapshot is not None
        rows,pixels,palettes=snapshot;tiles=TileCompositor();chosen=None
        for i in sorted(np.flatnonzero(rows[:,0]),key=lambda i:-int(rows[i,1]*rows[i,2])):
            w,h=map(int,rows[i,1:3]);a=pixels[i,:w*h].reshape(h,w)
            if all(not a[y:y+8,x:x+8].any() or tiles.find(a[y:y+8,x:x+8].tobytes()) for y in range(0,h,8) for x in range(0,w,8)):chosen=int(i);break
        assert chosen is not None,'no exact painted candidate in native capture'
        isolated=np.zeros_like(rows);isolated[chosen]=rows[chosen];request=(isolated,pixels,palettes)
        start=time.perf_counter()
        while not r.parts_renderer.runtime_requests and time.perf_counter()-start<30:
            r.parts_renderer.schedule_unknown(request);time.sleep(.02)
        assert r.parts_renderer.runtime_requests,r.parts_renderer.unmapped_misses
        binding=next(iter(r.parts_renderer.runtime_requests));reference=r.parts_renderer.prepared[binding].tobytes();core.set_ready_parts(r.parts_renderer);core.load(state);core.run()
        found=np.flatnonzero(core.parts[:,0]==binding);assert len(found)>0,'native dynamic identity did not match'
        assert not any(int(core.parts[i,7])&0x80000000 for i in found),'prepared image stayed native'
        image=r.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds);image.save(out/'dynamic_registered.png')
        del r.parts_renderer.prepared[binding];r.parts_renderer.cache.clear();r.parts_renderer.ready_generation+=1;core.set_ready_parts(r.parts_renderer);core.load(state);core.run()
        found=np.flatnonzero(core.parts[:,0]==binding);assert all(int(core.parts[i,7])&0x80000000 for i in found),'evicted image lost its native fallback'
        r.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds)
        start=time.perf_counter()
        while binding not in r.parts_renderer.prepared and time.perf_counter()-start<20:r.parts_renderer.collect_prepared();time.sleep(.02)
        assert r.parts_renderer.prepared[binding].tobytes()==reference,'recovered image changed'
        report=dict(actual_rom_texture=True,exact_native_material=True,binding=binding,source_groups=r.parts_renderer.registration_stats[binding]['tile_groups'],complete_tile_coverage=True,native_readiness_transition=True,eviction_fallback=True,lossless_cache_recovery=True)
        (out/'dynamic_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:core.close();r.parts_renderer.close()

if __name__=='__main__':main()
