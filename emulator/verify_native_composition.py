"""Exact visibility equivalence and actual warmed parts composition comparison."""
import json,time,csv
from unittest.mock import patch
import numpy as np
from PIL import Image
import native_composition as nc
from hd_core import Core,ROOT
from hd_parts import PartsRenderer

def compare_random():
    rng=np.random.default_rng(107);checks=0;times={'numpy':[],'native':[]}
    for iteration in range(2000):
        if iteration%20==0:
            layers=rng.integers(0,6,(192,256),dtype='uint8');owners=rng.integers(0,128,(192,256),dtype='uint8')
            bg=rng.integers(0,5,6,dtype='uint8');obj=rng.integers(0,4,128,dtype='uint16')
            old=nc.PartVisibility(layers,owners,bg,obj,native=False);new=nc.PartVisibility(layers,owners,bg,obj)
            assert new.api is not False
        x=int(rng.integers(0,255));y=int(rng.integers(0,191));w=int(rng.integers(1,min(128,256-x)+1));h=int(rng.integers(1,min(96,192-y)+1))
        kind=iteration%2;item=int(rng.integers(0,4 if kind else 128));priority=int(rng.integers(0,4));control=int(rng.integers(0,2**32,dtype='uint32'))
        # Force both alpha-background eligibility forms in half the cases.
        if iteration%4<2:control=(control&~0xc0)|0x40|(1<<(8+item if kind else 12))
        args=(x,y,x+w,y+h,priority,kind,item,control)
        start=time.perf_counter();a,astate=old.mask(*args);times['numpy'].append((time.perf_counter()-start)*1000)
        start=time.perf_counter();b,bstate=new.mask(*args);times['native'].append((time.perf_counter()-start)*1000)
        assert astate==bstate and np.array_equal(a,b),(iteration,args,astate,bstate)
        checks+=1
    return dict(random_exact_masks=checks,mask_mean_ms={k:round(float(np.mean(v)),5) for k,v in times.items()},mask_speedup=round(float(np.mean(times['numpy'])/np.mean(times['native'])),2))

def actual_checks():
    import hd_parts
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/performance/visibility_saves')
    renderer=PartsRenderer(async_prepare=False);rows=[];csv_rows=[]
    try:
        for name,path in [('ability','parts/result.state'),('cutin','font/cutin_dialogue.state'),('battle','attract/battle_13620.state')]:
            core.load(ROOT/'test_current'/path,refresh_code=True);core.run()
            attrs=np.frombuffer(core.obj.raw,dtype='<u2').reshape(128,4);priority=(attrs[:,2]>>10)&3
            baseline=nc.PartVisibility(core.ids,core.owners,core.bgpriors,priority,native=False)
            native=nc.PartVisibility(core.ids,core.owners,core.bgpriors,priority)
            for kind in (0,1):
                for i in range(4 if kind else 128):
                    for prio in range(4):
                        for control in (0,0x3f40,0xffffffff):
                            a,astate=baseline.mask(0,0,256,192,prio,kind,i,control);b,bstate=native.mask(0,0,256,192,prio,kind,i,control)
                            assert astate==bstate and np.array_equal(a,b),(name,kind,i,prio,control)
            # Full production composition comparison is enabled after the
            # independently verified helper is wired into hd_parts.compose.
            stats=dict(scene=name,actual_full_screen_priority_masks=1584)
            if hasattr(hd_parts,'PartVisibility'):
                reference=None;measurements={}
                for mode in ('numpy','native'):
                    api=nc.library() if mode=='native' else False
                    with patch.object(nc,'library',return_value=api):
                        values=[]
                        for run in range(12):
                            image=Image.fromarray(core.native[:192]).resize((1440,1080),Image.Resampling.NEAREST)
                            start=time.perf_counter();renderer.compose(image,core.parts,core.obj.raw,core.ids,core.owners,core.bgpriors,core.bgparts,core.part_palettes);elapsed=(time.perf_counter()-start)*1000
                            if run>=2:values.append(elapsed)
                        pixels=np.asarray(image)
                        if reference is None:reference=pixels.copy()
                        else:assert np.array_equal(reference,pixels),(name,'full compose differs')
                        measurements[mode]=round(float(np.mean(values)),3)
                stats.update(full_compose_ms=measurements,full_compose_pixel_exact=True)
            rows.append(stats)
        if hasattr(hd_parts,'PartVisibility'):
            hd_parts.SCALE=960/256;renderer.cache.clear();renderer.scaled.clear();renderer.material_maps.clear()
            for frame in range(24):
                core.run();core.audio.clear();reference=None
                for mode in ('numpy','native') if frame%2==0 else ('native','numpy'):
                    api=nc.library() if mode=='native' else False
                    with patch.object(nc,'library',return_value=api):
                        # Prepare any newly appearing sprite before measuring.
                        args=(core.parts,core.obj.raw,core.ids,core.owners,core.bgpriors,core.bgparts,core.part_palettes)
                        renderer.compose(Image.fromarray(core.native[:192]).resize((960,720),Image.Resampling.NEAREST),*args)
                        image=Image.fromarray(core.native[:192]).resize((960,720),Image.Resampling.NEAREST)
                        start=time.perf_counter();renderer.compose(image,*args);elapsed=(time.perf_counter()-start)*1000
                    pixels=np.asarray(image)
                    if reference is None:reference=pixels.copy()
                    else:assert np.array_equal(reference,pixels),('moving actual frame',frame)
                    csv_rows.append(dict(scene='battle_13620',advanced_frame=frame+1,mode=mode,compose_ms=round(elapsed,5),output_width=960,parts=int((core.parts[:,0]>0).sum()),bgparts=int((core.bgparts[:,0]>0).sum()),pixel_exact=True))
            path=ROOT/'test_current/performance/native_visibility_game_frames.csv'
            with path.open('w',newline='',encoding='utf-8') as stream:
                writer=csv.DictWriter(stream,fieldnames=list(csv_rows[0]));writer.writeheader();writer.writerows(csv_rows)
            rows.append(dict(scene='battle_13620_live_24frames',full_compose_ms={mode:round(float(np.mean([x['compose_ms'] for x in csv_rows if x['mode']==mode])),3) for mode in ('numpy','native')},full_compose_pixel_exact=True,csv=str(path.relative_to(ROOT))))
    finally:core.close();renderer.close()
    return rows

def main():
    report=compare_random();report['actual']=actual_checks()
    out=ROOT/'test_current/performance/native_visibility_verification.json';out.write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
