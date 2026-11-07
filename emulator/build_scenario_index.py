"""Precompute compact native signatures; play never decodes all background PNGs."""
import json,zlib,time
from pathlib import Path
import numpy as np
from PIL import Image
from hd_scenario_backgrounds import ROOT,rgb555

def main():
    start=time.perf_counter();folder=ROOT/'graphics/scenario_backgrounds';meta=json.loads((folder/'catalog.json').read_text(encoding='utf-8'))
    refs=[];names=[];heights=[];keys=[];xs=[];ys=[];resources=[]
    for row in meta['resources']:
        with Image.open(ROOT/'graphics'/row['native']) as opened:reference=rgb555(np.asarray(opened.convert('RGB')))
        h,w=reference.shape
        if w!=256 or h>256 or h<64:continue
        resource=len(names);names.append(row['name']);heights.append(h);padded=np.zeros((256,256),dtype='uint16');padded[:h]=reference;refs.append(padded)
        for x in (16,64,112,160,208):
            for y in range(0,h-7,8):
                patch=reference[y:y+8,x:x+8]
                if np.unique(patch).size<4:continue
                keys.append(zlib.crc32(patch.tobytes()));xs.append(x);ys.append(y);resources.append(resource)
    path=folder/'runtime_index.npz';tmp=folder/'runtime_index.tmp.npz'
    np.savez_compressed(tmp,names=np.array(names),heights=np.array(heights,dtype='uint16'),references=np.array(refs),keys=np.array(keys,dtype='uint32'),xs=np.array(xs,dtype='uint8'),ys=np.array(ys,dtype='uint8'),resources=np.array(resources,dtype='uint16'))
    tmp.replace(path);print(json.dumps(dict(backgrounds=len(names),anchors=len(keys),cache_bytes=path.stat().st_size,build_seconds=round(time.perf_counter()-start,3))))

if __name__=='__main__':main()
