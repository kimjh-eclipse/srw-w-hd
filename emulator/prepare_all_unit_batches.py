"""Pack source atlases into registered sheets for built-in AI restoration."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/all_units'
catalog=json.loads((OUT/'catalog.json').read_text());batches=[];segments=[];height=0;seen={};duplicates=[]
excluded={7152,13978,13983} # character cut-ins / text, outside unit-part scope
def flush():
    global segments,height
    if not segments:return
    size=(256,max(128,height));sheet=Image.new('RGBA',size);name=f'batch_{len(batches):03}'
    for p in segments:sheet.paste(Image.open(OUT/f"unit_{p['resource']}_native.png"),(0,p['batch_y']))
    sheet.resize((size[0]*8,size[1]*8),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    batches.append(dict(name=name,native_size=list(size),segments=segments,reference=f'{name}_reference.png',image=f'{name}_hd.png'))
    segments=[];height=0
for p in catalog['packages']:
    if p['resource'] in excluded:continue
    digest=hashlib.sha256((OUT/f"unit_{p['resource']}_native.png").read_bytes()).hexdigest()
    if digest in seen:duplicates.append(dict(resource=p['resource'],source=seen[digest]));continue
    seen[digest]=p['resource']
    if height+p['height']>256:flush()
    segments.append(dict(resource=p['resource'],batch_y=height,height=p['height'],width=p['width']))
    height+=p['height']
flush()
(OUT/'batches.json').write_text(json.dumps(dict(batches=batches,duplicates=duplicates,excluded=sorted(excluded)),indent=2))
print(json.dumps(dict(batches=len(batches),unique_packages=len(seen),duplicates=len(duplicates),excluded=sorted(excluded))))
