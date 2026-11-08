"""Plan palette-independent HD scene layers and install exact 2x2 art atlases."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import argparse,json,hashlib,shutil
from pathlib import Path
from collections import defaultdict
import numpy as np
from PIL import Image
ROOT=PROJECT_ROOT;F=ROOT/'graphics/battle_backgrounds'

def write(path,data):
    temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(data,indent=2));temp.replace(path)

def build():
    catalog=json.loads((F/'catalog.json').read_text());groups=defaultdict(list)
    for row in catalog['resources']:groups[row['geometry_sha256']].append(row)
    reuse={'battle_6761_6677_6695':'city','battle_6459_6467_6471':'field','battle_6761_6763_6764':'tower','battle_6581_6592_6594':'space','battle_6790_6793_6795':'deck'}
    families=[]
    for digest,rows in groups.items():
        def brightness(row):
            a=np.asarray(Image.open(ROOT/'graphics'/row['native']));valid=a[:,:,3]>0
            return float(a[:,:,:3][valid].mean()) if valid.any() else 0
        representative=next((r for r in rows if r['name'] in reuse),max(rows,key=brightness))
        owner=representative['name'];family=dict(owner=owner,geometry_sha256=digest,native_size=representative['native_size'],members=[r['name']for r in rows],reference=representative['reference'],native=representative['native'])
        indices=np.asarray(Image.open(ROOT/'graphics'/representative['indices']))
        if not indices.any():
            Image.new('RGBA',(representative['native_size'][0]*3,representative['native_size'][1]*3)).save(F/f'{owner}_hd.png')
            family.update(status='preserved_transparent',method='original empty layer')
        elif owner in reuse:
            name=reuse[owner];original=Image.open(ROOT/f'graphics/backgrounds/{name}_native.png');art=Image.open(ROOT/f'graphics/backgrounds/{name}_hd.png').convert('RGBA');w,h=representative['native_size']
            art.crop((0,0,round(art.width*w/original.width),round(art.height*h/original.height))).save(F/f'{owner}_hd.png')
            family.update(status='reused_existing_hd',source=f'backgrounds/{name}_hd.png',native_exact_match=True)
        else:family['status']='pending'
        for row in rows:
            row.update(art_owner=owner,image=f'battle_backgrounds/{owner}_hd.png',source_palette_rgb=representative['palette_rgb'],source_indices=representative['indices'],source_native=representative['native'],generated=(F/f'{owner}_hd.png').exists())
        families.append(family)
    batches=[];pending=defaultdict(list)
    for family in families:
        if family['status']=='pending':pending[tuple(family['native_size'])].append(family)
    for size,items in sorted(pending.items()):
        for i in range(0,len(items),4):
            group=items[i:i+4];w,h=size;atlas=Image.new('RGB',(w*2,h*2),'black');name=f'battle_quad_{len(batches):02}'
            for n,item in enumerate(group):atlas.paste(Image.open(ROOT/'graphics'/item['reference']).convert('RGB'),(n%2*w,n//2*h))
            atlas.resize((w*6,h*6),Image.Resampling.NEAREST).save(F/f'{name}_reference.png')
            batches.append(dict(name=name,owners=[g['owner']for g in group],columns=2,rows=2,native_size=list(size),reference=f'{name}_reference.png',selected=f'{name}_hd.png',status='pending'))
    write(F/'catalog.json',catalog);write(F/'families.json',dict(family_count=len(families),families=families));write(F/'batches.json',dict(tool='built-in image_gen',batches=batches));print('families',len(families),'pending',sum(len(v)for v in pending.values()),'batches',len(batches))

def install(name,source):
    meta=json.loads((F/'batches.json').read_text());batch=next(b for b in meta['batches'] if b['name']==name);shutil.copyfile(source,F/batch['selected']);art=Image.open(F/batch['selected']).convert('RGBA')
    for n,owner in enumerate(batch['owners']):art.crop((n%2*art.width//2,n//2*art.height//2,(n%2+1)*art.width//2,(n//2+1)*art.height//2)).save(F/f'{owner}_hd.png')
    batch.update(status='generated',source_path=source,generated_size=list(art.size),sha256=hashlib.sha256((F/batch['selected']).read_bytes()).hexdigest());write(F/'batches.json',meta)
    catalog=json.loads((F/'catalog.json').read_text())
    for row in catalog['resources']:row['generated']=(ROOT/'graphics'/row['image']).exists()
    write(F/'catalog.json',catalog);print(name,'installed',len(batch['owners']),'ready rows',sum(r['generated']for r in catalog['resources']))

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--install',nargs=2);args=parser.parse_args();install(*args.install) if args.install else build()
