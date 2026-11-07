"""Atomically publish a generated map into the live, reloadable index."""
import argparse,json,shutil,hashlib,msvcrt
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--map',type=int,required=True);parser.add_argument('--source',type=Path,required=True);args=parser.parse_args();folder=ROOT/'graphics/map_tiles'
    with (folder/'install.lock').open('a+b') as lock:
        if lock.tell()==0:lock.write(b'0');lock.flush()
        lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_LOCK,1)
        try:install(folder,args)
        finally:lock.seek(0);msvcrt.locking(lock.fileno(),msvcrt.LK_UNLCK,1)

def install(folder,args):
    catalogpath=folder/'catalog.json';catalog=json.loads(catalogpath.read_text());row=next(r for r in catalog['maps'] if r['id']==args.map);destination=folder/f'map_{args.map}_hd.png'
    if args.source.resolve()!=destination.resolve():shutil.copyfile(args.source,destination)
    row.update(image=destination.name,status='generated_runtime_indexed',image_sha256=hashlib.sha256(destination.read_bytes()).hexdigest())
    for candidate in catalog['maps']:
        image=folder/f"map_{candidate['id']}_hd.png"
        if image.exists():candidate.update(image=image.name,status='generated_runtime_indexed',image_sha256=hashlib.sha256(image.read_bytes()).hexdigest())
    catalog['generated_maps']=sum('image' in r for r in catalog['maps']);temp=catalogpath.with_suffix('.tmp.json');temp.write_text(json.dumps(catalog,indent=2));temp.replace(catalogpath)
    path=folder/'library.json';library=dict(maps=[r for r in catalog['maps'] if r.get('image')]);temp=path.with_suffix('.tmp.json');temp.write_text(json.dumps(library,indent=2));temp.replace(path)
    promptpath=folder/'generation_prompts.json';prompts=json.loads(promptpath.read_text()) if promptpath.exists() else dict(tool='built-in image_gen',prompt='Faithful complete top-down tactical-map HD redraw; preserve all original geography, colors, landmarks and exact positions. No grid, UI, text or units.',assets=[]);prompts['assets']=[r for r in prompts['assets'] if r['map']!=args.map]+[dict(map=args.map,reference=row['native'],image=destination.name,generated_source=str(args.source))];promptpath.write_text(json.dumps(prompts,indent=2));print('Indexed map',args.map,'total',len(library['maps']))

if __name__=='__main__':main()
