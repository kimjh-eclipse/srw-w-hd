"""Prebuild display-sized textures; no per-part PNG decoding during play."""
import json,zlib,time
from PIL import Image
import numpy as np
from hd_parts_registration import register_part
from menu_scene import ROOT,SCALE
from render_resolution import MAX_WIDTH,MAX_HEIGHT

def save_texture(image,path):
    image.save(path,compress_level=1)

def main():
    start=time.perf_counter();folder=ROOT/'graphics/menu_units';images={};groups=[]
    source=Image.open(folder/'name_card_generated.png').convert('RGBA').resize((MAX_WIDTH*2,MAX_HEIGHT),Image.Resampling.LANCZOS)
    for i,name in enumerate(('kazuma','aircraft')):
        art=source.crop((i*MAX_WIDTH,0,(i+1)*MAX_WIDTH,MAX_HEIGHT));save_texture(art,folder/(name+'_display.png'));images[name]=name+'_display.png'
    bgpath=ROOT/'graphics/backgrounds/library.json';library=json.loads(bgpath.read_text());entries=library['backgrounds']
    for layer,name,bid in [(2,'grid_front',9),(3,'grid_back',10)]:
        path=ROOT/f'test_current/menu_card/bg_0_{layer}.png';art=Image.open(path).convert('RGBA').resize((MAX_WIDTH,MAX_WIDTH),Image.Resampling.NEAREST)
        save_texture(art,folder/(name+'_display.png'));images[name]=name+'_display.png'
        # MenuScene receives live grid offsets from Core; these are supporting
        # textures, not independent native background replacements.
        entries[:]=[e for e in entries if e['id']!=bid]
    bgpath.write_text(json.dumps(library,indent=2))
    layout=json.loads((folder/'favorite_runtime.json').read_text());paint=Image.open(folder/'favorite_runtime_hd.png').convert('RGBA').resize((4096,1792),Image.Resampling.LANCZOS)
    meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());bindingids=[i for i,b in enumerate(meta['bindings'],1) if b.get('atlas_id')=='favorite_menu']
    for group in layout['groups']:
        bank=group['bank'];cx=(bank-1)%4*128;cy=(bank-1)//4*112;rect=(cx*8,cy*8,(cx+128)*8,(cy+112)*8)
        # Painted alpha survives intact; native pixels never clip the contour.
        art=paint.crop(rect).resize((round(128*SCALE),round(112*SCALE)),Image.Resampling.LANCZOS)
        name=f'favorite_{bank}';save_texture(art,folder/(name+'_display.png'));images[name]=name+'_display.png'
        offsets=[]
        for p in group['parts']:
            binding=next(i for i,b in enumerate(meta['bindings'],1) if b.get('atlas_id')=='favorite_menu' and b['hash']==p['hash'])
            offsets.append(dict(binding=binding,x=p['sheet_x']-cx,y=p['sheet_y']-cy))
        bounds=group['bounds']
        groups.append(dict(name=name,bank=bank,offsets=offsets,bounds=[bounds[0]-cx,bounds[1]-cy,bounds[2],bounds[3]]))
    spec=dict(images=images,groups=groups,favorite_bindings=bindingids,display_scale=SCALE,source_width=MAX_WIDTH,preparation_seconds=time.perf_counter()-start)
    (folder/'scene_runtime.json').write_text(json.dumps(spec,indent=2));print('Prepared display-sized menu textures in',round(time.perf_counter()-start,2),'seconds')

if __name__=='__main__':main()
