"""Install generated introduction layers and favorite units into runtime registries."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import hashlib,json,zlib
from pathlib import Path
import numpy as np
from PIL import Image
from hd_parts_registration import register_part

ROOT=PROJECT_ROOT

def main():
    folder=ROOT/'graphics/menu_units'; report={}
    bgpath=ROOT/'graphics/backgrounds/library.json'
    library=json.loads(bgpath.read_text()); entries=library['backgrounds']
    paint=Image.open(folder/'name_card_generated.png').convert('RGBA').resize((4096,1536),Image.Resampling.LANCZOS)
    native=Image.open(folder/'name_card_native.png').convert('RGBA')
    for layer,name in enumerate(('name_card_kazuma','name_card_aircraft')):
        reference=native.crop((layer*256,0,(layer+1)*256,192))
        art,quality=register_part(paint.crop((layer*2048,0,(layer+1)*2048,1536)),reference)
        # Full tilemap coordinates, retaining the game's separate layer masks.
        full=Image.new('RGBA',(4096,4096));full.paste(art,(0,0))
        full.save(folder/(name+'_hd.png'))
        raw=np.load(ROOT/f'test_current/menu_card/bg_0_{layer}.npz')
        maps=raw['map']; tile_size=64 if raw['info'][0]&128 else 32
        indices=np.unique(maps.view('<u2')&1023); count=(int(indices.max())+1)*tile_size
        selected=raw['tiles'][:count].reshape(-1,tile_size)[indices].tobytes()
        source=ROOT/f'test_current/menu_card/bg_0_{layer}.png'
        Image.open(source).save(folder/(name+'_native.png'))
        existing=next((e for e in entries if e['name']==name),None)
        bid=existing['id'] if existing else max(e['id'] for e in entries)+1
        item=dict(id=bid,name=name,layer=layer,image=f'menu_units/{name}_hd.png',native=f'menu_units/{name}_native.png',tile_bytes=count,tile_size=tile_size,tile_indices=indices.tolist(),signatures=[[zlib.crc32(selected),zlib.crc32(maps.tobytes())]],periodic=False)
        if existing: entries[entries.index(existing)]=item
        else:entries.append(item)
        report[name]=quality
    bgpath.write_text(json.dumps(library,indent=2))
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings']
    prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    layout=json.loads((folder/'favorite_runtime.json').read_text())
    source=Image.open(folder/'favorite_runtime_native.png').convert('RGBA')
    paint=Image.open(folder/'favorite_runtime_hd.png').convert('RGBA').resize((4096,1792),Image.Resampling.LANCZOS)
    atlas=Image.new('RGBA',(4096,2048)); ref=Image.new('RGBA',(512,256)); number=0
    name='favorite_menu'; meta['atlases'][name]=dict(image='menu_units/favorite_parts_hd.png',reference='menu_units/favorite_parts_native.png',native_size=[512,256],lazy=True)
    for group in layout['groups']:
        bank=group['bank'];cx=((bank-1)%4)*128;cy=((bank-1)//4)*112
        rect=(cx,cy,cx+128,cy+112)
        registered,quality=register_part(paint.crop(tuple(v*8 for v in rect)),source.crop(rect))
        report['favorite_bank_'+str(bank)]=quality
        for part in group['parts']:
            x=(number%8)*64;y=(number//8)*64;number+=1
            sx=part['sheet_x']-cx;sy=part['sheet_y']-cy;w=part['w'];h=part['h']
            crop=registered.crop((sx*8,sy*8,(sx+w)*8,(sy+h)*8))
            if part['b']&4096:crop=crop.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if part['b']&8192:crop=crop.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            original=Image.open(ROOT/f"test_current/formation/part_{part['oam']}.png").convert('RGBA')
            # Clamp each hardware part to its own source silhouette after unflipping.
            crop.putalpha(original.getchannel('A').resize(crop.size,Image.Resampling.BICUBIC))
            atlas.paste(crop,(x*8,y*8));ref.paste(original,(x,y))
            colors=np.load(ROOT/f"test_current/formation/part_{part['oam']}.npz")['palette']
            rgb=[[(int(c)>>(5*k)&31)*255//31 for k in range(3)] for c in colors]
            item=dict(hash=part['hash'],index_hash=part['index_hash'],x=x,y=y,w=w,h=h,atlas_id=name,original_palette_rgb=rgb,auto_animation=True,dynamic_palette=False,indexed_safe=False)
            old=next((i for i,b in enumerate(bindings) if b.get('atlas_id')==name and b['hash']==item['hash']),None)
            if old is None:bindings.append(item)
            else:bindings[old]=item
    atlas.save(folder/'favorite_parts_hd.png');ref.save(folder/'favorite_parts_native.png')
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(meta));temporary.replace(path)
    report['favorite_parts']=number;report['approved_prefix_preserved']=True
    (folder/'installed.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
