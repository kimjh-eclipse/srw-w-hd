import json,time,tracemalloc
import numpy as np
from PIL import Image
from hd_map_icons import MapIconRenderer,ROOT

def main():
    out=ROOT/'test_current/map_icons';tracemalloc.start();started=time.perf_counter();r=MapIconRenderer();initialization_seconds=time.perf_counter()-started;memory_current,memory_peak=tracemalloc.get_traced_memory();tracemalloc.stop();reports=[]
    # The first frames show a warp orb rather than a visible source icon.
    # menu_step_1 has its rendered craft already beyond the left edge, while
    # its post-frame OAM is not a reliable description of the visible frame.
    expected={'map_fresh':0,'menu_step_0':0,'menu_step_1':0,'menu_step_2':1,'menu_step_3':1,'menu_step_4':1,'menu_step_5':1,'grid':0}
    for name,expected_count in expected.items():
        frame=np.asarray(Image.open(out/(name+'_native.png')));native=frame[192:384];image=Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST)
        before=time.perf_counter();count=r.compose(image,native);seconds=time.perf_counter()-before;image.save(out/(name+'_hd.png'))
        reports.append(dict(scene=name,matches=r.last_matches,seconds=seconds));print(name,count,round(seconds*1000,2),'ms',r.last_matches,flush=True)
        assert count==expected_count,(name,expected_count,r.last_matches)
        if expected_count:assert r.last_matches[0]['resource']==4253 and r.last_matches[0]['x']==32 and r.last_matches[0]['y']==88
    frame=np.asarray(Image.open(out/'live_500.png'));native=frame[192:384];image=Image.fromarray(native).resize((1440,1080),Image.Resampling.NEAREST);r.compose(image,native);image.save(out/'live_500_hd.png')
    assert {(m['resource'],m['palette'],m['x'],m['y']) for m in r.last_matches}=={(3950,3939,96,0),(4253,3938,96,144)},r.last_matches
    reports.append(dict(scene='live_500',matches=r.last_matches))
    assert not r.prepare_errors,r.prepare_errors
    # All real source icons and all five affiliation palettes must retain an
    # exact recognisable identity. An unrelated frame must not match any.
    failures=[];equivalent_variants=[];palettes=list(r.palettes);cases=0
    resources=list(r.indices)
    for palette in palettes:
        for flip in range(4):
            for begin in range(0,len(resources),64):
                native=np.full((192,256,3),(3,7,11),dtype='uint8');colors=r.palettes[palette].astype('uint8');expected_icons=[]
                for slot,resource in enumerate(resources[begin:begin+64]):
                    idx=r.indices[resource];source=idx[::-1] if flip&2 else idx
                    if flip&1:source=source[:,::-1]
                    x=(slot%16)*16;y=(slot//16)*24+16;patch=colors[source].copy();mask=source>0;crop=native[y:y+16,x:x+16];crop[mask]=patch[mask];expected_icons.append((resource,x,y))
                matches=r.recognize(native);actual={(m['resource'],m['x'],m['y']) for m in matches}
                for resource,x,y in expected_icons:
                    cases+=1
                    if (resource,x,y) not in actual:
                        local=[m for m in matches if m['x']==x and m['y']==y];equivalent=False
                        expected=r.indices[resource]
                        if flip&2:expected=expected[::-1]
                        if flip&1:expected=expected[:,::-1]
                        for match in local:
                            observed=r.indices[match['resource']]
                            if match['flip']&2:observed=observed[::-1]
                            if match['flip']&1:observed=observed[:,::-1]
                            if np.array_equal(expected>0,observed>0) and np.array_equal(colors[expected],r.palettes[match['palette']].astype('uint8')[observed]):equivalent=True
                        row=dict(resource=resource,palette=palette,flip=flip,x=x,y=y,matches=local)
                        if equivalent:equivalent_variants.append(row)
                        else:failures.append(row)
    assert not failures[:1],failures[:3]
    blank=np.random.default_rng(1).integers(0,256,(192,256,3),dtype='uint8');assert not r.recognize(blank)
    warm_native=np.asarray(Image.open(out/'menu_step_5_native.png'))[192:];warm_target=Image.fromarray(warm_native).resize((1440,1080));r.compose(warm_target,warm_native);samples=[]
    for _ in range(30):
        start=time.perf_counter();r.compose(warm_target,warm_native);samples.append(time.perf_counter()-start)
    report=dict(actual_scenes=reports,synthetic_cases=cases,synthetic_failures=failures,equivalent_mirrored_variants=len(equivalent_variants),false_positive_random_frame=False,prepared_errors=r.prepare_errors,generated_nonempty_icons=len(r.indices),initialization_seconds=initialization_seconds,initialization_allocated_bytes=memory_current,initialization_peak_bytes=memory_peak,warm_composition_mean_ms=float(np.mean(samples)*1000),warm_composition_p95_ms=float(np.percentile(samples,95)*1000))
    (out/'verification.json').write_text(json.dumps(report,indent=2));print('verified',cases,'palette cases')

if __name__=='__main__':main()
