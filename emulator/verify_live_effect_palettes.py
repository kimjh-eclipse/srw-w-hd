"""Check real battle palette/transform snapshots against original used indices."""
import base64,json,zlib
import numpy as np
from hd_core import Core,ROOT
from hd_parts import PartsRenderer

def main():
    renderer=PartsRenderer();core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/parts/saves')
    rows=[];seen=set();old_unused=0
    try:
        for name,offset,length,limit in [(n,0,30,6) for n in ('target','battle_13110','battle_13350','battle_13620','battle_13920','battle_14850')]+[('battle_14850',3300,600,100),('battle_14850',7380,660,100),('battle_14850',8460,960,100)]:
            core.load(ROOT/f'test_current/attract/{name}.state');count=0
            for _ in range(offset):core.run();core.audio.clear()
            for frame in range(length):
                core.run();core.audio.clear()
                for slot in np.flatnonzero(core.parts[:,0]):
                    row=core.parts[slot].copy();bid=int(row[0]);spec=renderer.bindings[bid-1]
                    if not spec.get('dynamic_palette'):continue
                    key=(bid,int(row[4]),int(row[1])&0x700,int(row[2])&0x3000)
                    if key in seen:continue
                    seen.add(key);art=renderer.sprite(row,core.obj.raw,core.part_palettes[slot]);base_row=row.copy();base_row[4]=spec['hash'];reference=renderer.sprite(base_row,core.obj.raw,core.part_palettes[slot])
                    assert np.array_equal(np.asarray(art.getchannel('A')),np.asarray(reference.getchannel('A'))),'Recolor changed alpha'
                    source=renderer.scaled[spec.get('source_binding',bid)];palette=np.asarray(spec.get('palette_source_rgb',spec['original_palette_rgb']),dtype='float32')
                    used=renderer.used_palette_indices(bid,palette,spec)
                    if used is None or not len(used):continue
                    _,indices=renderer.material_map(bid,source,palette,spec);assert set(np.unique(indices))<=set(used)
                    rgb=np.asarray(source)[:,:,:3].astype('float32');q=np.rint(rgb*31/255).astype('uint32');unrestricted=renderer.get_palette_lut(palette)[q[:,:,0]|q[:,:,1]<<5|q[:,:,2]<<10];bad=int(np.count_nonzero(~np.isin(unrestricted,used)&(np.asarray(source)[:,:,3]>0)));old_unused+=bad
                    rows.append(dict(state=name,frame=offset+frame,binding=bid,native_palette_hash=int(row[4]),used_indices=used.tolist(),previous_opaque_pixels_using_unused_slots=bad,alpha_unchanged=True));count+=1
                    if count>=limit:break
                if count>=limit:break
        assert rows
        report=dict(real_battle_palette_cases=len(rows),old_opaque_pixels_using_unrelated_slots=old_unused,new_pixels_using_unrelated_slots=0,alpha_and_geometry_preserved=True,cases=rows)
        (ROOT/'test_current/parts/live_effect_palette_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='cases'}))
    finally:core.close();renderer.close()

if __name__=='__main__':main()
