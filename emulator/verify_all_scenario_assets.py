"""Resolve every installed scenario texture through the real runtime matcher."""
import json,time
import numpy as np
from PIL import Image
from hd_core import ROOT
from hd_scenario_backgrounds import ScenarioBackgrounds,rgb555

def main():
    out=ROOT/'test_current/scene_assets';meta=json.loads((ROOT/'graphics/scenario_backgrounds/catalog.json').read_text(encoding='utf-8'))
    renderer=ScenarioBackgrounds(async_prepare=False);rows=[]
    try:
        for item in meta['resources']:
            if not (ROOT/'graphics'/item['image']).exists():continue
            with Image.open(ROOT/'graphics'/item['native']) as opened:source=np.asarray(opened.convert('RGB'))
            native=np.zeros((192,256,3),dtype='uint8');h=min(192,source.shape[0]);native[:h]=source[:h]
            target=Image.fromarray(native).resize((960,720),Image.Resampling.NEAREST)
            # This verification uses the same full-reference registration as
            # actual play, separately from the campaign-frame tests.
            start=time.perf_counter();changed=renderer.compose(target,native);match=renderer.last_match
            blank=np.unique(source.reshape(-1,3),axis=0).shape[0]==1
            matched=False
            if match:
                reference=renderer.sources[match['name']][1];dy=match['source_offset_y'];upper=max(0,-dy);lower=min(h,len(reference)-dy)
                matched=upper==0 and lower==h and np.array_equal(rgb555(native[:h]),reference[dy:dy+h])
            rows.append(dict(name=item['name'],runtime_match=match,exact_visible_source=matched,flat_color=blank,ms=round((time.perf_counter()-start)*1000,2)))
        report=dict(installed=len(rows),matched=sum(r['exact_visible_source'] for r in rows),flat_color=sum(r['flat_color'] for r in rows),failed=[r['name'] for r in rows if not r['exact_visible_source'] and not r['flat_color']],cases=rows,full_campaign_playthrough=False)
        (out/'all_scenario_runtime.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='cases'}))
    finally:renderer.close()

if __name__=='__main__':main()
