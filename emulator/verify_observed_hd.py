"""Check exact observed scenes, scrolling backgrounds and foreground retention."""
import json,time
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from hd_renderer import HDRenderer

def main():
    folder=ROOT/'test_current/attract';out=ROOT/'test_current/parts';results=[]
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True);r=HDRenderer(async_parts=True,dynamic_parts=True)
    try:
        for name in ['target','battle_13110','battle_13620','battle_14850']:
            core.load(folder/(name+'.state'));core.set_ready_parts(r.parts_renderer)
            # Warm the exact starting scene as well as advancing animation.
            # This distinguishes source loading from missing bindings.
            started=time.perf_counter();quiet=0
            while time.perf_counter()-started<40:
                core.load(folder/(name+'.state'));core.set_ready_parts(r.parts_renderer);core.run();core.audio.clear()
                r.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,unknown=core.unknown_snapshot())
                quiet=quiet+1 if not r.parts_renderer.pending and not r.parts_renderer.unmapped_pending else 0
                if quiet>=3:break
                time.sleep(.02)
            unknown=core.unknown_snapshot()
            if unknown is not None:
                rows,raw,palettes=unknown
                folder_out=out/'unknown';folder_out.mkdir(exist_ok=True)
                entries=[]
                for i in np.flatnonzero(rows[:,0]):
                    key,w,h,a,b,c,_,fnv=map(int,rows[i]);idx=raw[i,:w*h].reshape(h,w);pal=palettes[i].astype('uint32');colors=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1)
                    Image.fromarray(np.dstack([colors[idx].astype('uint8'),(idx!=0).astype('uint8')*255])).save(folder_out/f'{key}_{fnv}.png')
                    entries.append(dict(identity=[key,fnv],w=w,h=h,a=a,b=b,c=c))
                (folder_out/(name+'.json')).write_text(json.dumps(entries,indent=2))
            samples=[]
            for f in range(90):
                core.set_ready_parts(r.parts_renderer);core.run();core.audio.clear();t=time.perf_counter()
                image=r.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,unknown=core.unknown_snapshot())
                samples.append((time.perf_counter()-t)*1000)
                if f==0:image.save(out/(name+'_hd.png'))
            core.load(folder/(name+'.state'));core.set_ready_parts(r.parts_renderer);core.run()
            image=r.render_top(core.native,core.ids,core.hd,parts=core.parts,obj=core.obj.raw,owners=core.owners,bgpriors=core.bgpriors,bgparts=core.bgparts,part_palettes=core.part_palettes,backgrounds=core.backgrounds,unknown=core.unknown_snapshot());image.save(out/(name+'_warm_hd.png'))
            results.append(dict(scene=name,backgrounds=r.backgrounds.last_matches,render_median_ms=float(np.median(samples)),render_p99_ms=float(np.percentile(samples,99)),prepared=len(r.parts_renderer.prepared),errors=r.parts_renderer.prepare_errors,dynamic_registered=len(r.parts_renderer.runtime_requests),dynamic_pending=len(r.parts_renderer.unmapped_pending),dynamic_misses=[dict(identity=list(k),**v) for k,v in r.parts_renderer.unmapped_misses.items()]))
            print(results[-1],flush=True)
    finally:r.parts_renderer.close();core.close()
    (out/'observed_hd_verification.json').write_text(json.dumps(results,indent=2))

if __name__=='__main__':main()
