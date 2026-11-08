"""Replay painted key-color contamination with unchanged native transparency."""
import json,subprocess,types
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_parts import PartsRenderer
from hd_renderer import HDRenderer

def main():
    source=subprocess.check_output(['git','show','f150c8ba:emulator/hd_parts.py']).decode('utf8')
    old=types.ModuleType('parts_before');old.__file__=str(ROOT/'emulator/hd_parts.py');exec(compile(source,old.__file__,'exec'),old.__dict__)
    before=old.PartsRenderer();after=PartsRenderer();core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/saves');rows=[]
    try:
        for name in ('bonta_attack','bonta_cutin','eid_attack'):
            core.load(ROOT/f'test_current/combat/{name}.state');core.run();changed=0;parts=0
            for i in np.flatnonzero(core.parts[:,0]):
                row=core.parts[i];a=before.sprite(row,core.obj.raw,core.part_palettes[i]);b=after.sprite(row,core.obj.raw,core.part_palettes[i])
                assert np.array_equal(np.asarray(a.getchannel('A')),np.asarray(b.getchannel('A'))),(name,int(i),'alpha changed')
                aa=np.asarray(a);bb=np.asarray(b);changed+=int(np.count_nonzero(np.any(aa[:,:,:3]!=bb[:,:,:3],axis=2)&(bb[:,:,3]>0)));parts+=1
            rows.append(dict(scene=name,parts=parts,corrected_opaque_pixels=changed,alpha_unchanged=True))
        assert sum(row['corrected_opaque_pixels'] for row in rows)>0
        core.load(ROOT/'test_current/combat/bonta_cutin.state');core.run()
        renderer=HDRenderer(gpu_composition=True);renderer.parts_renderer.close()
        kw=dict(parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds)
        old.SCALE=renderer.size[0]/256
        for parts in (before,after):parts.cache.clear();parts.scaled.clear();parts.material_maps.clear()
        pink=[]
        for parts in (before,after):
            renderer.parts_renderer=parts;image=renderer.render_top(core.native,core.ids,core.hd,**kw)
            rgb=np.asarray(image)[:480]
            pink.append(int(np.count_nonzero((rgb[:,:,0]>180)&(rgb[:,:,2]>80)&(rgb[:,:,2]>rgb[:,:,1]*1.05))))
        assert pink[0]>0 and pink[1]==0,pink
        image.save(ROOT/'test_current/combat/bonta_cutin_fixed.png')
        report=dict(scenes=rows,bonta_unintended_pink_pixels_before=pink[0],bonta_unintended_pink_pixels_after=pink[1])
        (ROOT/'test_current/combat/edge_palette_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
    finally:core.close();before.close();after.close()

if __name__=='__main__':main()
