"""Prepare and publish only the tactical-map generation range 32..66."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
from PIL import Image
ROOT=PROJECT_ROOT;F=ROOT/'graphics/map_tiles';LOG=F/'icon_agent_generation.json'
PROMPT='Edit target is a strict production atlas containing TWO independent top-down tactical-map images side by side, split exactly at 50% width. Redraw both reference maps as clean high-resolution hand-painted Japanese mecha strategy-game terrain. Preserve ALL landforms, roads, cliffs, coastlines, buildings, vegetation, rocks, object counts, scale, colors and exact XY positions in each map. Strict orthographic overhead view; no perspective, isometric angle, horizon or camera tilt. The maps remain square and independently framed, equal in size; do not crop, enlarge, shift, merge or rearrange any map feature. Do not add terrain, roads, buildings or objects. Smooth natural terrain detail and crisp fine mechanical edges, no pixels or blur. No grid lines, text, labels, UI, units, characters, mechs, markers, captions, gutters, borders or separator lines. Keep the exact 2:1 atlas aspect ratio and the central seam at exactly 50% width. Every source map detail must be redrawn, not copied as pixel art.'

def prepare():
    jobs=json.loads((F/'generation_jobs.json').read_text());assigned=jobs[32:67];pairs=[]
    for number in range(0,len(assigned),2):
        rows=assigned[number:number+2];actual=len(rows)
        if len(rows)==1:rows=rows*2
        name=f'icon_pair_{number//2:02}';canvas=Image.new('RGB',(1088,544))
        for n,row in enumerate(rows):canvas.paste(Image.open(F/row['reference']).convert('RGB'),(n*544,0))
        canvas.resize((1632,816),Image.Resampling.NEAREST).save(F/(name+'_reference.png'))
        pairs.append(dict(name=name,job_indices=list(range(32+number,32+number+actual)),maps=[r['representative'] for r in rows],unique_outputs=actual,reference=name+'_reference.png',generated=name+'_hd.png',status='pending'))
    LOG.write_text(json.dumps(dict(tool='built-in image_gen',assigned_jobs=[32,66],source_count=35,prompt=PROMPT,pairs=pairs),indent=2));print('prepared',len(pairs),'pairs')

def install(name,source):
    log=json.loads(LOG.read_text());row=next(r for r in log['pairs'] if r['name']==name);assert 0<=int(name.split('_')[-1])<18
    target=F/row['generated'];shutil.copyfile(source,target);image=Image.open(target).convert('RGB');saved=[]
    for n,mid in enumerate(row['maps'][:row['unique_outputs']]):
        output=F/f'map_{mid}_hd.png';image.crop((n*image.width//2,0,(n+1)*image.width//2,image.height)).save(output)
        subprocess.run([sys.executable,str(ROOT/'scripts/assets/install_map_art.py'),'--map',str(mid),'--source',str(output)],check=True)
        saved.append(dict(map=mid,file=output.name,size=list(Image.open(output).size),sha256=hashlib.sha256(output.read_bytes()).hexdigest()))
    row.update(status='generated_runtime_indexed',source_path=str(source),generated_size=list(image.size),outputs=saved,atlas_sha256=hashlib.sha256(target.read_bytes()).hexdigest());log['generated_maps']=sum(r.get('unique_outputs',0) for r in log['pairs'] if r['status']=='generated_runtime_indexed');LOG.write_text(json.dumps(log,indent=2));print(name,'indexed',log['generated_maps'],'/35')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--prepare',action='store_true');p.add_argument('--install',nargs=2);a=p.parse_args()
    prepare() if a.prepare else install(*a.install)
