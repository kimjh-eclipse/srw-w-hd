"""Build two-panel HD production references and install generated atlases."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import argparse,json,shutil
from pathlib import Path
from PIL import Image
ROOT=PROJECT_ROOT;F=ROOT/'graphics/scenario_backgrounds'
PROMPT="""Edit target: exact production game background atlas with TWO separate rectangular scenes stacked vertically, each occupying exactly half the height. Redraw both reference backgrounds as clean high resolution hand-painted Japanese mecha anime environment art. Preserve the exact subject identity, composition, perspective, colors, lighting, structural positions, object count, horizon and vanishing points in EACH panel. Do not rearrange, crop, enlarge or move any element. No gutters, borders or separator lines: the top panel ends at exactly 50% height and the lower panel begins there. All sharp smooth contours, painted material details, no pixelation, blur or noise. No people, robots, portraits, dialogue windows, UI, extra objects, decorations, captions or added text. Preserve any original tiny architectural signs as abstract illegible marks, not new words. Output a vertical 8:13 atlas at 1024x1664 pixels or larger. This will be split into two registered runtime background layers. Every quadrant must be finished, not a sketch or pixel upscale."""

def write(path,value):
    tmp=path.with_suffix('.tmp.json');tmp.write_text(json.dumps(value,indent=2));tmp.replace(path)

def build():
    catalog=json.loads((F/'catalog.json').read_text());planned=[r for r in catalog['resources'] if r['map_resource']>=5102 and not (ROOT/'graphics'/r['image']).exists() and r['native_size']==[256,208]]
    priority=[5309,5312,5321,5324,5327,5330,5336,5342,5360,5363,5369,5399,5411,5414,5417,5423,5429,5435,5438,5459,5462,5465,5468,5477,5495,5498,5501,5504,5507,5519]
    planned.sort(key=lambda r:(priority.index(r['map_resource']) if r['map_resource'] in priority else len(priority)+r['map_resource']))
    batches=[]
    for i in range(0,len(planned),4):
        rows=planned[i:i+4]
        while len(rows)<4:rows.append(rows[-1])
        name=f'quad_{i//4:02}';im=Image.new('RGB',(512,416))
        for n,r in enumerate(rows):im.paste(Image.open(ROOT/'graphics'/r['native']).convert('RGB'),(n%2*256,n//2*208))
        im.resize((1536,1248),Image.Resampling.NEAREST).save(F/(name+'_reference.png'))
        batches.append(dict(name=name,resources=[r['map_resource'] for r in rows],columns=2,rows=2,reference=f'{name}_reference.png',selected=f'{name}_hd.png',prompt=PROMPT.replace('TWO separate rectangular scenes stacked vertically, each occupying exactly half the height','FOUR separate rectangular scenes in an exact 2x2 grid').replace('1024x1664','1536x1248'),status='pending'))
    write(F/'quad_batches.json',dict(tool='built-in image_gen',batches=batches));print('planned',len(planned),'backgrounds in',len(batches),'four-panel calls')

def install(name,source):
    batchfile=F/('quad_batches.json' if name.startswith('quad') else 'batches.json')
    meta=json.loads(batchfile.read_text());batch=next(b for b in meta['batches'] if b['name']==name)
    target=F/batch['selected'];shutil.copyfile(source,target);image=Image.open(target).convert('RGB')
    cols=batch.get('columns',1);rows=batch.get('rows',2)
    for n,i in enumerate(batch['resources']):image.crop(((n%cols)*image.width//cols,(n//cols)*image.height//rows,(n%cols+1)*image.width//cols,(n//cols+1)*image.height//rows)).save(F/f'scenario_{i}_hd.png')
    batch.update(status='generated',source_path=str(source),generated_size=list(image.size),panel_size=[image.width//cols,image.height//rows]);write(batchfile,meta)
    catalog=json.loads((F/'catalog.json').read_text())
    for r in catalog['resources']:
        r.update(id=r['map_resource'],resource=r['image_resource'],generated=(ROOT/'graphics'/r['image']).exists(),category='scenario_background' if r['map_resource']>=5102 else 'story_cg_or_map')
        r['status']='generated' if r['generated'] else 'native_only'
    catalog.update(generated=sum(r['generated'] for r in catalog['resources']),scenario_backgrounds=141,scenario_backgrounds_generated=sum(r['generated'] for r in catalog['resources'] if r['map_resource']>=5102))
    write(F/'catalog.json',catalog);write(F/'library.json',dict(backgrounds=catalog['resources']));print(name,'installed',batch['resources'],'panels',batch['panel_size'],'total',catalog['scenario_backgrounds_generated'],'/141')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--install',nargs=2);a=p.parse_args()
    install(*a.install) if a.install else build()
