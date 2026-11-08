"""Bake the existing exact icon palette transfer once, before gameplay."""
import hashlib,json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

def main():
    folder=ROOT/'graphics/map_icons';path=folder/'library.json';meta=json.loads(path.read_text());records=[r for r in meta['records'] if r.get('prepared')]
    palettes={int(k):np.asarray(v,dtype='int16')[:,:3] for k,v in meta['palettes'].items()};ids=sorted(palettes);colors=palettes[3938]
    out=np.empty((len(records),len(ids),60,60,4),dtype='uint8');sources={}
    for i,row in enumerate(records):
        source=folder/row['prepared'];sources[str(row['resource'])]=hashlib.sha256(source.read_bytes()).hexdigest()
        with Image.open(source) as image:pixels=np.array(image.convert('RGBA'))
        assert pixels.shape==(60,60,4),source
        rgb=pixels[:,:,:3].astype('int16');nearest=np.argmin(((rgb.astype('float32')[:,:,None,:]-colors[None,None,:,:])**2).sum(-1),axis=2)
        for j,palette in enumerate(ids):
            out[i,j]=pixels
            if palette!=3938:out[i,j,:,:,:3]=np.clip(rgb+palettes[palette][nearest]-colors[nearest],0,255).astype('uint8')
    temporary=folder/'runtime_textures.tmp.npy';np.save(temporary,out);temporary.replace(folder/'runtime_textures.npy')
    (folder/'runtime_textures.json').write_text(json.dumps(dict(signature=hashlib.sha256(path.read_bytes()).hexdigest(),resources=[r['resource'] for r in records],palettes=ids,sources=sources),indent=2))
    print(json.dumps(dict(resources=len(records),palettes=len(ids),bytes=out.nbytes)))

if __name__=='__main__':main()
