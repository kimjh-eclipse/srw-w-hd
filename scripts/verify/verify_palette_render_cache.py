
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,hashlib,sys
import numpy as np
from hd_parts import PartsRenderer,ROOT

def main():
    baseline='--baseline' in sys.argv;r=PartsRenderer();results=[];chosen=[]
    for flag in ('auto_unit','auto_full_attack','auto_shared_attack'):
        chosen.extend([i for i,b in enumerate(r.bindings,1) if b.get(flag) and b.get('dynamic_palette') and b['w']>=16 and b['h']>=16][:2])
    for binding in chosen:
        spec=r.bindings[binding-1];rgb=np.asarray(spec['original_palette_rgb'],dtype='float32');five=np.rint(rgb*31/255).astype('uint16');palette=five[:,0]|five[:,1]<<5|five[:,2]<<10
        for n,target in enumerate((palette,np.zeros(16,dtype='uint16'),palette&31,(palette&1023)|31<<10)):
            row=[binding,0,4096 if n==3 else 0,0,123+n,0,16,0];art=r.sprite(row,bytes(1024),target);results.append([binding,n,hashlib.sha256(art.tobytes()).hexdigest()])
    out=ROOT/'test_current/parts'
    if baseline:(out/'palette_render_reference.json').write_text(json.dumps(results));print('saved pixel reference',len(results))
    else:
        assert results==json.loads((out/'palette_render_reference.json').read_text());report=dict(cases=len(results),pixel_identical=True,includes_black_recolor_and_flip=True);(out/'palette_render_cache_verification.json').write_text(json.dumps(report,indent=2));print(report)
    r.close()

if __name__=='__main__':main()
