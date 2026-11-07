"""Install only inspected, generated portraits; never touches cut-ins or ROM."""
import json,zlib
import numpy as np
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/portraits'
def main():
    portraits=[]
    observed_matches={x['name']:x['img'] for x in json.loads((OUT/'archive/observed_matches.json').read_text()) if x['error']==0}
    for plan in ('observed.json','observed_extra.json','observed_archive.json'):
        path=OUT/plan
        if not path.exists():continue
        for source in json.loads(path.read_text())['portraits']:
            image=OUT/source['image']
            if not image.exists():continue
            native=Image.open(OUT/(source['name']+'_native.png')).convert('RGB')
            x,y,w,h=source['rectangle']
            assert native.size==(w,h),(source['name'],native.size)
            # Ignore only HUD margins; the whole face must be an exact native
            # match. This also recognizes the same expression in another panel.
            content=np.asarray(native.crop((5,2,48,46)))>>3
            source=dict(source,match_format='rgb5')
            img=source.get('archive_img',observed_matches.get(source['name']))
            if img is not None:source['portrait_mask']=f'portraits/archive/portrait_{img:05}_native.png'
            portraits.append(dict(**source,path='portraits/'+source['image'],
                match_rectangle=[x+5,y+2,43,44],content_crc32=zlib.crc32(content.tobytes())))
    assert len({p['name'] for p in portraits})==len(portraits)
    temporary=OUT/'library.json.tmp'
    temporary.write_text(json.dumps(dict(portraits=portraits),indent=2))
    temporary.replace(OUT/'library.json')
    print(json.dumps(dict(portraits=len(portraits))))
if __name__=='__main__':main()
