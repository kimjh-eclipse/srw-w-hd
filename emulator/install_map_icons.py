"""Prepare tiny display-sized AI icon textures and exact native lookup data."""
import json,sys,time
from pathlib import Path
import numpy as np
from PIL import Image
from hd_core import ROOT

def main():
    folder=ROOT/'graphics/map_icons';path=folder/'library.json';library=json.loads(path.read_text());records=library['records'];prepared=folder/'prepared';prepared.mkdir(exist_ok=True)
    atlas={};indices=[];ids=[];quality=[]
    for r in records:
        if r['duplicate_of'] is not None:continue
        idx=np.load(folder/f"icon_{r['resource']}_indices.npy")
        if not idx.any():r['empty']=True;continue
        indices.append(idx);ids.append(r['resource'])
        number=r['sheet'];source=folder/f'sheet_{number:02}_hd.png'
        if not source.exists():continue
        if number not in atlas:atlas[number]=Image.open(source).convert('RGBA').resize((2048,1024),Image.Resampling.LANCZOS)
        cell=r['cell'];x=cell%8*256;y=cell//8*256;art=atlas[number].crop((x,y,x+256,y+256));a=np.array(art)
        # Decoder noise has alpha 1–3; normalize opaque cel body alpha while
        # retaining the generated anti-aliased contour. No native-mask clip.
        a[:,:,3]=np.clip((a[:,:,3].astype('float32')-16)*255/235,0,255).astype('uint8');art=Image.fromarray(a)
        ys,xs=np.where(a[:,:,3]>96);ny,nx=np.where(idx>0)
        assert len(xs)>32 and len(nx)>8,r
        bounds=(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)
        target=(round(nx.min()*90/16),round(ny.min()*90/16),round((nx.max()+1)*90/16),round((ny.max()+1)*90/16))
        canvas=Image.new('RGBA',(90,90));crop=art.crop(bounds).resize((target[2]-target[0],target[3]-target[1]),Image.Resampling.LANCZOS);canvas.paste(crop,target[:2]);canvas.save(prepared/f"{r['resource']}.png",compress_level=1)
        r['prepared']=f"prepared/{r['resource']}.png";quality.append(dict(resource=r['resource'],body_bounds=bounds,target_bounds=target))
    np.savez_compressed(folder/'native_indices.npz',indices=np.array(indices),resources=np.array(ids))
    for sheet in library['sheets']:sheet['generated_ready']=(folder/sheet['generated']).exists()
    library['prepared_count']=len(quality);library['empty_count']=sum(bool(r.get('empty')) for r in records);library['complete']=len(quality)+library['empty_count']==library['unique_icons'];library['body_alpha_threshold']=16
    path.write_text(json.dumps(library,indent=2));(folder/'registration.json').write_text(json.dumps(quality,indent=2));print('prepared',len(quality),'icons; complete',library['complete'])

if __name__=='__main__':main()
