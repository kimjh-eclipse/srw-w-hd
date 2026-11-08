"""Precompute original part palette membership without changing HD textures."""
import hashlib,json
from collections import OrderedDict
from pathlib import Path
import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parent.parent

def main():
    raw=(ROOT/'graphics/kazuma_parts_library.json').read_bytes();library=json.loads(raw);bindings=library['bindings'];masks=np.zeros(len(bindings),dtype='uint16')
    references=OrderedDict();signatures={};cache={};known=0
    for index,spec in enumerate(bindings):
        if not spec.get('dynamic_palette') or spec.get('index_pixels'):continue
        source_id=spec.get('source_binding',index+1);source=bindings[source_id-1];name=source.get('atlas_id','base')
        palette=np.asarray(spec.get('palette_source_rgb',spec.get('original_palette_rgb',library.get('source_palette_rgb',[]))),dtype='float32')
        key=(source_id,palette.tobytes())
        if key not in cache:
            meta=library.get('atlases',{}).get(name,{'reference':'kazuma_parts_atlas_reference.png'})
            image=references.pop(name,None)
            try:
                path=ROOT/'graphics'/meta['reference']
                if image is None:
                    signatures[name]=hashlib.sha256(path.read_bytes()).hexdigest()
                    with Image.open(path) as opened:image=opened.convert('RGBA')
                    size=tuple(meta.get('native_size',(256,128)))
                    if image.size!=size:image=image.resize(size,Image.Resampling.NEAREST)
                references[name]=image
                while len(references)>8:references.popitem(last=False)
                x,y,w,h=(source[k] for k in ('x','y','w','h'));pixels=np.asarray(image.crop((x,y,x+w,y+h)));colors=pixels[:,:,:3][pixels[:,:,3]>0]
                five=np.rint(colors.astype('float32')*31/255).astype('uint32');codes=five[:,0]|five[:,1]<<5|five[:,2]<<10
                native=np.rint(palette*31/255).astype('uint32');slots=native[:,0]|native[:,1]<<5|native[:,2]<<10
                used=np.flatnonzero(np.isin(slots,np.unique(codes)));cache[key]=sum(1<<int(i) for i in used if 0<i<16)
            except (OSError,ValueError,KeyError):cache[key]=0
        masks[index]=cache[key];known+=bool(masks[index])
    folder=ROOT/'graphics';np.save(folder/'material_slots.npy',masks,allow_pickle=False)
    (folder/'material_slots.json').write_text(json.dumps(dict(library_sha256=hashlib.sha256(raw).hexdigest(),references=signatures,bindings=len(bindings),cached_bindings=known),indent=2))
    print(json.dumps(dict(bindings=len(bindings),cached_bindings=known,bytes=masks.nbytes)))

if __name__=='__main__':main()
