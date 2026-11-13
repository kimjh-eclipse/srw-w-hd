"""Register every captured name-menu plane and retain painted alpha contours."""
import json,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from painted_edges import clean_alpha


def main():
    folder=ROOT/'graphics/menu_units';captures=ROOT/'test_current/menu_card/configuration'
    specpath=folder/'scene_runtime.json';spec=json.loads(specpath.read_text());basis=spec.get('source_width',960);scale=basis/256
    for name in ('pilot','warship'):
        art=clean_alpha(Image.open(folder/f'config_{name}_generated.png').convert('RGBA')).resize((basis,round(basis*.75)),Image.Resampling.LANCZOS)
        native=Image.open(folder/f'config_{name}_native.png').convert('RGBA')
        pixels=np.asarray(art.getchannel('A').resize((256,192),Image.Resampling.BOX))>64;expected=np.asarray(native.getchannel('A'))>0
        iou=float((pixels&expected).sum()/max(1,(pixels|expected).sum()))
        assert iou>=.80,(name,'generated geometry differs',iou)
        rgba=np.array(art);rgba[rgba[:,:,3]==0]=0;Image.fromarray(rgba).save(folder/f'config_{name}_hd.png',optimize=True)
        spec['images'][f'configuration_{name}']=f'config_{name}_hd.png'
    aircraft=Image.open(folder/'aircraft_display.png').convert('RGBA');shifted=Image.new('RGBA',aircraft.size);shifted.paste(aircraft,(0,round(24*scale)))
    shifted.save(folder/'config_aircraft_hd.png',optimize=True);spec['images']['configuration_aircraft']='config_aircraft_hd.png'
    library_path=ROOT/'graphics/backgrounds/library.json';library=json.loads(library_path.read_text());entries=library['backgrounds']
    pictures={};report=[]
    for selection in ('overview','pilot','aircraft','warship','weapon'):
        for layer in (0,1):
            source=captures/selection/f'bg_0_{layer}.png';native=Image.open(source).convert('RGBA')
            if not native.crop((0,0,256,192)).getchannel('A').getbbox():continue
            picture=(('kazuma' if layer==0 else 'aircraft') if selection in ('overview','weapon') else f'configuration_{selection}')
            raw=np.load(captures/selection/f'bg_0_{layer}.npz');maps=raw['map'];size=64 if int(raw['info'][0])&128 else 32
            indices=np.unique(maps.view('<u2')&1023);count=(int(indices.max())+1)*size
            selected=raw['tiles'][:count].reshape(-1,size)[indices].tobytes();signature=[zlib.crc32(selected),zlib.crc32(maps.tobytes())]
            name=f'name_configuration_{selection}_{layer}';existing=next((e for e in entries if e['name']==name),None)
            bid=existing['id'] if existing else max(e['id'] for e in entries)+1
            reference=f'config_{selection}_{layer}_native.png';pixels=np.array(native);pixels[pixels[:,:,3]==0]=0;Image.fromarray(pixels).save(folder/reference)
            item=dict(id=bid,name=name,layer=layer,image='menu_units/'+spec['images'][picture],native='menu_units/'+reference,
                tile_bytes=count,tile_size=size,tile_indices=indices.tolist(),signatures=[signature],periodic=False,menu_configuration=picture)
            if existing:entries[entries.index(existing)]=item
            else:entries.append(item)
            pictures[str(bid)]=picture;report.append(dict(selection=selection,layer=layer,id=bid,picture=picture))
    spec['configuration_pictures']={'7':'kazuma','8':'aircraft',**pictures}
    library_path.write_text(json.dumps(library,indent=2));specpath.write_text(json.dumps(spec,indent=2))
    (folder/'configuration_registration.json').write_text(json.dumps(dict(planes=report,painted_alpha=True),indent=2));print(report)


if __name__=='__main__':main()
