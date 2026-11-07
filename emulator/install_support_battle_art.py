import json,hashlib,shutil,sys
from pathlib import Path
from PIL import Image
F=Path(__file__).resolve().parent.parent/'graphics/battle_backgrounds'
def install(name,source,prompt):
 b=next(x for x in json.loads((F/'batches.json').read_text())['batches'] if x['name']==name)
 shutil.copyfile(source,F/b['selected']);art=Image.open(F/b['selected']).convert('RGBA')
 for n,owner in enumerate(b['owners']):art.crop((n%2*art.width//2,n//2*art.height//2,(n%2+1)*art.width//2,(n//2+1)*art.height//2)).save(F/f'{owner}_hd.png')
 p=F/'support_generation.json';j=json.loads(p.read_text()) if p.exists() else {'tool':'built-in image_gen','batches':[]};j['batches']=[x for x in j['batches'] if x['name']!=name];j['batches'].append(dict(name=name,source_path=source,selected=b['selected'],owners=b['owners'],prompt=prompt,generated_size=list(art.size),sha256=hashlib.sha256((F/b['selected']).read_bytes()).hexdigest()));p.write_text(json.dumps(j,indent=2));print(name,'saved',len(b['owners']))
if __name__=='__main__':install(*sys.argv[1:])
