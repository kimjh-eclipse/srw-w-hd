"""Exhaust the shared cut-in/part blend contract and registered cut-in routes."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import itertools,json
import numpy as np
from hd_core import ROOT
from native_composition import PartVisibility

def main():
    checks=0
    for kind,item,layer,bgprio,priority,mode,first,second,weight in itertools.product(range(2),range(4),range(4),range(4),range(4),range(4),range(2),range(2),range(17)):
        # A scalar native-layer fixture isolates each priority/blend decision.
        layers=np.full((1,1),layer,dtype='uint8');bg=np.full(6,bgprio,dtype='uint8')
        control=(mode<<6)|(first<<layer)|(second<<(8+item if kind else 12))
        v=PartVisibility(layers,np.zeros_like(layers),bg,np.zeros(128,dtype='uint16'))
        base=bgprio>priority or (bgprio==priority and (not kind or layer>item))
        alpha=mode==1 and first and second
        visible=base or alpha
        foreground=bgprio<priority or (kind and bgprio==priority and layer<item)
        expected=(255*weight//16 if alpha and foreground else 255) if visible else 0
        actual,_=v.mask(0,0,1,1,priority,kind,item,control,weight<<8)
        assert int(actual[0,0])==expected,(kind,item,layer,bgprio,priority,control,weight,int(actual[0,0]),expected)
        checks+=1
    library=json.loads((ROOT/'graphics/cutins_library.json').read_text())
    routes=[dict(id=1,name='kazuma',route='dedicated foreground overlay')]
    for item in library['cutins']:
        assert (ROOT/'graphics'/item['image']).is_file()
        assert (ROOT/'graphics'/item.get('reference','portraits/'+item['name']+'_native.png')).is_file()
        routes.append(dict(id=item['id'],name=item['name'],layer=item['layer'],route='native foreground visibility mask'))
    report=dict(shared_obj_bg_blend_cases=checks,second_target_coefficients=list(range(17)),registered_cutin_routes=routes,generic_cutins='All BG layers use the shared native priority and blend path.',scope='Exhaustive compositor combinations; not a replay of every campaign cut-in.')
    (ROOT/'test_current/combat/cutin_composition_audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
