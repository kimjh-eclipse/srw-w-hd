"""Register the actual Earth-region tilemap, including its Korean art label."""
import json,zlib
import numpy as np
from PIL import Image
from hd_core import ROOT

def main():
    folder=ROOT/'graphics/backgrounds';source=ROOT/'test_current/scene_assets/story'
    raw=np.load(source/'bg_0_3.npz');maps=raw['map'];size=64 if raw['info'][0]&128 else 32
    idx=np.unique(maps.view('<u2')&1023);count=(int(idx.max())+1)*size
    data=raw['tiles'][:count].reshape(-1,size)[idx].tobytes()
    reference=Image.open(source/'bg_0_3.png').convert('RGB');reference.save(folder/'earth_region_native.png')
    # 256x192 viewport occupies the upper part of the actual 256x256 map.
    canvas=reference.resize((1440,1440),Image.Resampling.NEAREST)
    art=Image.open(folder/'earth_region_hd.png').convert('RGB').resize((1440,1080),Image.Resampling.LANCZOS);canvas.paste(art,(0,0));canvas.save(folder/'earth_region_atlas.png',compress_level=1)
    path=folder/'library.json';meta=json.loads(path.read_text());entries=meta['backgrounds'];entries[:]=[b for b in entries if b['name']!='earth_region']
    item=dict(id=11,name='earth_region',layer=3,image='backgrounds/earth_region_atlas.png',native='backgrounds/earth_region_native.png',tile_size=size,tile_bytes=count,tile_indices=idx.tolist(),signatures=[[zlib.crc32(data),zlib.crc32(maps.tobytes())]],periodic=False)
    entries.append(item);path.write_text(json.dumps(meta,indent=2))
    prompt=dict(tool='built-in image_gen',source='earth_region_reference.png',image='earth_region_hd.png',translation={'地球圏エリア':'지구권 지역'},prompt='Redraw the supplied Earth-region background as clean HD anime science-fiction art; preserve orbital ellipse, Earth, Moon, satellites, colony positions and 4:3 framing. Replace the upper-left Japanese label with 지구권 지역. No other UI.')
    (folder/'earth_region_generation.json').write_text(json.dumps(prompt,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Registered Earth-region background',item['signatures'])

if __name__=='__main__':main()
