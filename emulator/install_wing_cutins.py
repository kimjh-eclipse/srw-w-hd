"""Install SCR-derived cut-ins with native clipping and registered silhouettes."""
import json
from PIL import Image
from hd_parts_registration import register_part
from hd_core import ROOT

def main():
    out=ROOT/'graphics/wing_parts';path=ROOT/'graphics/cutins_library.json';library=json.loads(path.read_text());records=[]
    for source in json.loads((out/'cutin_sources.json').read_text()):
        name=source['name'];native=Image.open(out/(name+'_cutin_native.png')).convert('RGBA');paint=Image.open(out/(name+'_cutin_generated.png')).convert('RGBA')
        art,stats=register_part(paint,native,scale=4);art.resize((960,720),Image.Resampling.LANCZOS).save(out/(name+'_cutin_registered.png'))
        existing=next((item for item in library['cutins'] if item['name']==name+'_wing'),None)
        identifier=existing['id'] if existing else max([1]+[item['id'] for item in library['cutins']])+1
        item=dict(id=identifier,name=name+'_wing',layer=1,layers=[0,1,2,3],native_size=[256,192],image='wing_parts/'+name+'_cutin_registered.png',reference='wing_parts/'+name+'_cutin_native.png',signatures=[source['signature']],resource=source['resource'],registration=stats)
        if existing:existing.update(item)
        else:library['cutins'].append(item)
        records.append(item)
    path.write_text(json.dumps(library,indent=2));(out/'cutin_installed.json').write_text(json.dumps(records,indent=2));print([(r['name'],r['id'],r['registration']) for r in records])

if __name__=='__main__':main()
