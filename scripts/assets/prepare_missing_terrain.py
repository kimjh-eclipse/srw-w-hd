"""Pack only native terrain identities absent from every generated world."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=PROJECT_ROOT;FOLDER=ROOT/'graphics/map_tiles';OUT=FOLDER/'missing_batches'

def canonical(p):return min(p.tobytes(),p[:,::-1].tobytes(),p[::-1].tobytes(),p[::-1,::-1].tobytes())

def main():
    OUT.mkdir(exist_ok=True);catalog=json.loads((FOLDER/'catalog.json').read_text());known=set()
    for row in catalog['maps']:
        if not (FOLDER/f"map_{row['id']}_hd.png").exists():continue
        q=np.asarray(Image.open(FOLDER/row['native']).convert('RGB'))>>3;h,w=q.shape[:2]
        for y in range(0,h-7,8):
            for x in range(0,w-7,8):known.add(canonical(q[y:y+8,x:x+8]))
    missing={};contexts={};count=0
    for row in catalog['maps']:
        if (FOLDER/f"map_{row['id']}_hd.png").exists():continue
        native=np.asarray(Image.open(FOLDER/row['native']).convert('RGB'));q=native>>3;h,w=q.shape[:2]
        for y in range(0,h-7,8):
            for x in range(0,w-7,8):
                key=canonical(q[y:y+8,x:x+8])
                if key in known:continue
                count+=1
                if key in missing:continue
                cx=x//16*16;cy=y//16*16;context=native[cy:cy+16,cx:cx+16];ckey=context.tobytes();contexts.setdefault(ckey,dict(map=row['id'],x=cx,y=cy,pixels=context));missing[key]=ckey
    # Existing contexts cover several missing subtiles. Drop contexts whose
    # missing identities were all covered by an earlier context.
    rows=[];covered=set(known)
    for row in contexts.values():
        q=row['pixels']>>3;keys=[canonical(q[y:y+8,x:x+8]) for y in (0,8) for x in (0,8)]
        if all(k in covered for k in keys):continue
        rows.append(row);covered.update(keys)
    batches=[]
    for first in range(0,len(rows),256):
        selected=rows[first:first+256];canvas=Image.new('RGB',(256,256));entries=[]
        for i,row in enumerate(selected):
            x=i%16*16;y=i//16*16;canvas.paste(Image.fromarray(row['pixels']),(x,y));entries.append(dict(map=row['map'],source_x=row['x'],source_y=row['y'],x=x,y=y,w=16,h=16))
        name=f'terrain_missing_{first//256:02}';canvas.save(OUT/(name+'_native.png'));canvas.resize((1536,1536),Image.Resampling.NEAREST).save(OUT/(name+'_reference.png'));batches.append(dict(name=name,native=f'missing_batches/{name}_native.png',reference=f'missing_batches/{name}_reference.png',image=f'missing_batches/{name}_hd.png',entries=entries,status='pending'))
    (OUT/'batches.json').write_text(json.dumps(batches,indent=2));print(json.dumps(dict(uncovered_occurrences=count,unique_missing_8x8=len(missing),context_regions=len(rows),batches=len(batches))))

if __name__=='__main__':main()
