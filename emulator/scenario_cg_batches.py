"""Plan and install the remaining 106 story CG and localized map backgrounds."""
import argparse,json,shutil
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;F=ROOT/'graphics/scenario_backgrounds'

def write(path,data):
    temporary=path.with_suffix('.tmp.json');temporary.write_text(json.dumps(data,indent=2));temporary.replace(path)

def build():
    catalog=json.loads((F/'catalog.json').read_text());rows=[r for r in catalog['resources'] if r['map_resource']<5102 and not (ROOT/'graphics'/r['image']).exists()]
    assert len(rows)==104
    maps=[4790,4791,4792,4793,4794,4800,4803,4806]
    rows.sort(key=lambda r:maps.index(r['map_resource']) if r['map_resource'] in maps else len(maps)+r['map_resource'])
    batches=[]
    for i in range(0,len(rows),4):
        group=rows[i:i+4];name=f'cg_{i//4:02}';atlas=Image.new('RGB',(512,384))
        for n,row in enumerate(group):
            image=Image.open(ROOT/'graphics'/row['native']).convert('RGB');assert image.size==(256,192)
            atlas.paste(image,(n%2*256,n//2*192))
        atlas.resize((1536,1152),Image.Resampling.NEAREST).save(F/f'{name}_reference.png')
        batches.append(dict(name=name,resources=[r['map_resource'] for r in group],columns=2,rows=2,reference=f'{name}_reference.png',selected=f'{name}_hd.png',status='pending',tool='built-in image_gen'))
    write(F/'cg_batches.json',dict(total_cg_or_map_resources=106,preexisting_reused_or_solid=[4797,5099],batches=batches));print('planned',len(rows),'in',len(batches),'atlases')

def install(name,source):
    path=F/'cg_batches.json';meta=json.loads(path.read_text());batch=next(b for b in meta['batches'] if b['name']==name);shutil.copyfile(source,F/batch['selected']);image=Image.open(F/batch['selected']).convert('RGB')
    for n,i in enumerate(batch['resources']):image.crop((n%2*image.width//2,n//2*image.height//2,(n%2+1)*image.width//2,(n//2+1)*image.height//2)).save(F/f'scenario_{i}_hd.png')
    batch.update(status='generated',source_path=str(source),generated_size=list(image.size));write(path,meta)
    catalog=json.loads((F/'catalog.json').read_text())
    for row in catalog['resources']:
        row['generated']=(ROOT/'graphics'/row['image']).exists();row['status']='generated' if row['generated'] else 'native_only'
    catalog.update(generated=sum(row['generated'] for row in catalog['resources']),story_cg_or_maps=106,story_cg_or_maps_generated=sum(row['generated'] for row in catalog['resources'] if row['map_resource']<5102))
    write(F/'catalog.json',catalog);write(F/'library.json',dict(backgrounds=catalog['resources']));print(name,'installed',batch['resources'],'all',catalog['generated'],'/247')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',nargs=2);args=p.parse_args();install(*args.install) if args.install else build()
