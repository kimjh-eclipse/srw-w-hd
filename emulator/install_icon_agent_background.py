"""Install only the background atlas range assigned to the map-icon agent."""
import json,shutil,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;F=ROOT/'graphics/scenario_backgrounds'

def main():
    name,source=sys.argv[1:];assert 20<=int(name.split('_')[1])<=31
    batch=next(b for b in json.loads((F/'quad_batches.json').read_text())['batches'] if b['name']==name)
    shutil.copyfile(source,F/(name+'_hd.png'));image=Image.open(F/(name+'_hd.png')).convert('RGB')
    for n,resource in enumerate(batch['resources']):
        box=((n%2)*image.width//2,(n//2)*image.height//2,(n%2+1)*image.width//2,(n//2+1)*image.height//2)
        image.crop(box).save(F/f'scenario_{resource}_hd.png')
    path=F/'icon_agent_generation.json';meta=json.loads(path.read_text()) if path.exists() else dict(tool='built-in image_gen',assigned_batches=[20,31],batches=[])
    row=dict(name=name,resources=batch['resources'],source_path=str(source),image=name+'_hd.png',generated_size=list(image.size),panels=[f'scenario_{r}_hd.png' for r in batch['resources']],status='generated',prompt='Exact production 2x2 background atlas. Redraw all four reference scenes as smooth HD Japanese mecha anime environment art, preserve exact composition/palette/perspective/object placements; 16:13 aspect ratio; no UI, text, people, additions or panel borders; pure-black panels stay black.')
    meta['batches']=[b for b in meta['batches'] if b['name']!=name]+[row];meta['generated_backgrounds']=sum(len(b['resources']) for b in meta['batches']);path.write_text(json.dumps(meta,indent=2));print(name,batch['resources'],'prepared',meta['generated_backgrounds'],'/48')

if __name__=='__main__':main()
