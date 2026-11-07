"""Compare every native pixel/identity across reloads and changing battle palettes."""
import sys,json,zlib,ctypes as C
from hd_core import Core,ROOT
from frame_compositor import ReadyParts

def main():
    baseline='--baseline' in sys.argv;out=ROOT/'test_current/parts';core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'cache_saves');records=[]
    try:
        ready=ReadyParts();core.set_ready_parts(ready)
        for name in ('target','battle_13110','battle_13620','battle_14850','cutin_2','target'):
            core.load(ROOT/f'test_current/attract/{name}.state')
            for frame in range(90):
                core.run();core.audio.clear();digest=zlib.crc32(core.native.tobytes())
                for array in (core.parts,core.bgparts,core.ids,core.owners,core.part_palettes):digest=zlib.crc32(array.tobytes(),digest)
                records.append([name,frame,digest])
        if baseline:(out/'native_cache_reference.json').write_text(json.dumps(records));print('saved native baseline',len(records))
        else:
            expected=json.loads((out/'native_cache_reference.json').read_text());assert expected==records,[(a,b) for a,b in zip(expected,records) if a!=b][:3]
            stats=(C.c_uint*6)();core.api.retro_srw_texture_cache_stats(stats)
            report=dict(frames=len(records),identical_native_pixels_and_metadata=True,includes_palette_changes_and_state_reload=True,obj_checks=stats[0],obj_hits=stats[1],obj_misses=stats[2],bg_checks=stats[3],bg_hits=stats[4],bg_misses=stats[5]);assert stats[1]>0 and stats[4]>0;print(report);(out/'native_cache_verification.json').write_text(json.dumps(report,indent=2))
    finally:core.close()

if __name__=='__main__':main()
