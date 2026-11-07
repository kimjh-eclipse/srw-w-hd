"""Register generated observed texture sheets, preserving existing binding IDs."""
import json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/observed_parts'

def main():
    path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text());bindings=meta['bindings'];prefix=hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest();known={b['hash'] for b in bindings if b.get('rgb_enabled',True) and not b.get('disabled')}
    quality=[];added=0
    for sheet in json.loads((OUT/'sheets.json').read_text())['sheets']:
        name=sheet['name'];paint=OUT/f'{name}_hd.png'
        if not paint.exists():continue
        image=Image.open(paint).convert('RGBA');native=Image.open(OUT/f'{name}_native.png').convert('RGBA')
        a=np.asarray(image.resize(native.size,Image.Resampling.LANCZOS))[:,:,3]>64;b=np.asarray(native)[:,:,3]>64;iou=float((a&b).sum()/max(1,(a|b).sum()))
        assert iou>.50,(name,iou)
        quality.append(dict(name=name,alpha_iou=iou));meta['atlases'][name]=dict(image=f'observed_parts/{name}_hd.png',reference=f'observed_parts/{name}_native.png',native_size=sheet['native_size'],lazy=True)
        for segment in sheet['segments']:
            for variant in segment['variants']:
                if variant['hash'] in known:continue
                bindings.append(dict(hash=variant['hash'],index_hash=variant['index_hash'],x=segment['x'],y=segment['y'],w=segment['w'],h=segment['h'],atlas_id=name,original_palette_rgb=segment['source']['palette_rgb'],palette_rgb=variant['palette_rgb'],observed_generated=True,dynamic_palette=False,indexed_safe=False))
                known.add(variant['hash']);added+=1
    assert len(bindings)<100000
    assert prefix==hashlib.sha256(json.dumps(bindings[:5263],sort_keys=True).encode()).hexdigest()
    sources={}
    for index,binding in enumerate(bindings,1):
        if not binding.get('observed_generated'):continue
        key=(binding['atlas_id'],binding['x'],binding['y'],binding['w'],binding['h'])
        if key in sources:binding['source_binding']=sources[key]
        else:sources[key]=index
    if added:
        temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(meta,indent=2));temporary.replace(path)
    report=dict(sheets=len(quality),added_bindings=added,total_bindings=len(bindings),quality=quality,prefix_preserved=True)
    (OUT/'installed.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
