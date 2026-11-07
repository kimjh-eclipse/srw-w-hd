"""Prepare small identity arrays; runtime opens only the winning world's art."""
import json,hashlib
from collections import defaultdict
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;FOLDER=ROOT/'graphics/map_tiles';OUT=FOLDER/'runtime_index'

def main():
    OUT.mkdir(exist_ok=True);catalog=json.loads((FOLDER/'catalog.json').read_text());index=defaultdict(list);metadata={};mini=[]
    for row in catalog['maps']:
        mid=row['id'];source=np.asarray(Image.open(FOLDER/row['native']).convert('RGB'))>>3;np.save(OUT/f'world_{mid}.npy',source);h,w=source.shape[:2];local=defaultdict(list)
        for y in range(0,h-15,16):
            for x in range(0,w-15,16):
                key=int.from_bytes(hashlib.blake2b(source[y+1:y+16,x+1:x+16].tobytes(),digest_size=8).digest(),'little');local[key].append((mid,x,y))
        for key,coords in local.items():
            if len(coords)<=8:index[key].extend(coords)
        overview=np.asarray(Image.open(FOLDER/row['overview_native']).convert('RGB'))>>3;mh,mw=overview.shape[:2];anchors=[]
        for y in range(0,mh-7,16):
            for x in range(0,mw-7,16):
                patch=overview[y:y+8,x:x+8]
                if len(np.unique(patch.reshape(-1,3),axis=0))>8:anchors.append((float(patch.astype('float32').std()),x,y))
        metadata[str(mid)]=dict(source_sha256=row['source_sha256'],source=f'world_{mid}.npy',overview_index=len(mini),overview_size=[mw,mh],anchors=[[x,y] for _,x,y in sorted(anchors,reverse=True)[:6]])
        mini.append(overview)
    maxh=max(a.shape[0] for a in mini);maxw=max(a.shape[1] for a in mini);minimap=np.zeros((len(mini),maxh,maxw,3),'uint8')
    for i,a in enumerate(mini):minimap[i,:a.shape[0],:a.shape[1]]=a
    np.save(OUT/'overviews.npy',minimap);keys=np.array(sorted(index),dtype='uint64');offsets=[];coords=[]
    for key in keys:
        rows=index[int(key)];offsets.append([len(coords),len(rows)]);coords.extend(rows)
    np.save(OUT/'keys.npy',keys);np.save(OUT/'offsets.npy',np.asarray(offsets,dtype='uint32'));np.save(OUT/'coordinates.npy',np.asarray(coords,dtype='uint16'));(OUT/'index.json').write_text(json.dumps(dict(version=1,maps=metadata),indent=2));print('Compiled',len(metadata),'maps;',len(keys),'landmark identities;',len(coords),'coordinates')

if __name__=='__main__':main()
