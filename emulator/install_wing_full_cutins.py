"""Register complete pilot layers identified from real battle VRAM captures."""
import json,shutil
from pathlib import Path
import numpy as np
from PIL import Image
from hd_core import ROOT
from hd_parts_registration import register_part

def main():
    folder=ROOT/'graphics/wing_parts';path=ROOT/'graphics/cutins_library.json'
    library=json.loads(path.read_text());records=[]
    for name,resource,frame,layer in (
        ('duo_full',22808,300000,2),('quatre_full',24993,300001,1),('duo_smile',24987,300003,1)):
        target=folder/(name+'_generated.png')
        if not target.exists():raise FileNotFoundError(f'Generate {target.name} from {name}_reference.png first.')
        native=Image.open(folder/(name+'_native.png')).convert('RGBA')
        paint=Image.open(target).convert('RGBA');art,stats=register_part(paint,native,scale=4)
        art.resize((960,720),Image.Resampling.LANCZOS).save(folder/(name+'_registered.png'),optimize=True)
        capture=np.load(ROOT/f'test_current/attract/bg_{frame}_{layer}.npz')
        base=int.from_bytes(capture['map'].tobytes()[:2],'little')&1023
        signature=2166136261
        for value in capture['tiles'][base*32+1024:base*32+3072]:signature=((signature^int(value))*16777619)&0xffffffff
        existing=next((x for x in library['cutins'] if x['name']==name),None)
        identifier=existing['id'] if existing else max(x['id'] for x in library['cutins'])+1
        item=dict(id=identifier,name=name,layer=layer,layers=[0,1,2,3],native_size=[256,192],image='wing_parts/'+name+'_registered.png',reference='wing_parts/'+name+'_native.png',signatures=[signature],resource=resource,registration=stats)
        if existing:existing.update(item)
        else:library['cutins'].append(item)
        records.append(item)
    path.write_text(json.dumps(library,indent=2));(folder/'full_cutin_installed.json').write_text(json.dumps(records,indent=2));print(records)

if __name__=='__main__':main()
