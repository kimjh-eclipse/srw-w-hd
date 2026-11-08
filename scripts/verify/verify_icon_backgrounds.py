"""Every prepared icon must replace its complete matte, not just source ink."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import numpy as np
from PIL import Image
from hd_map_icons import MapIconRenderer,ROOT

def main():
    renderer=MapIconRenderer();reports=[];background=Image.new('RGB',(256,192),(121,133,147))
    for resource in renderer.records:
        native=np.full((192,256,3),(0,0,132),dtype='uint8')
        idx=renderer.indices[resource];mask=idx>0;patch=native[48:64,64:80];patch[mask]=renderer.palettes[3938][idx[mask]]
        # Isolate composition from deliberately equivalent icon identities.
        entry=next(i for i,e in enumerate(renderer.entries) if e['resource']==resource and e['palette']==3938 and not e['flip'])
        renderer.recognize=lambda _,e=entry,r=resource:[dict(x=64,y=48,entry=e,resource=r,palette=3938,flip=0)]
        result=Image.fromarray(native);renderer.compose(result,native,background=background)
        expected=background.crop((64,48,80,64));art=renderer.texture(resource,3938,0,16);expected.paste(art,(0,0),art)
        assert np.array_equal(np.asarray(result)[48:64,64:80],np.asarray(expected)),resource
        reports.append(resource)
    (ROOT/'test_current/map_icons/background_verification.json').write_text(json.dumps(dict(icons=len(reports),all_mattes_restored=True)))
    print('Background replacement passed for',len(reports),'prepared icons')

if __name__=='__main__':main()
