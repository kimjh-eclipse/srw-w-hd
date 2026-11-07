import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;FOLDER=ROOT/'graphics/map_tiles'

def main():
    out=FOLDER/'front_batches';out.mkdir(exist_ok=True);jobs=json.loads((FOLDER/'generation_jobs.json').read_text());pending=[j for j in jobs[:32] if not (FOLDER/f"map_{j['representative']}_hd.png").exists()];batches=[]
    for i in range(0,len(pending),2):
        rows=pending[i:i+2];canvas=Image.new('RGB',(544,544*len(rows)));items=[]
        for y,row in enumerate(rows):
            image=Image.open(FOLDER/row['reference']).convert('RGB');canvas.paste(image.resize((544,544),Image.Resampling.NEAREST),(0,y*544));items.append(dict(map=row['representative'],img=row['img'],pal=row['pal'],slot=y))
        name=f'front_pair_{i//2:02}';canvas.save(out/(name+'_reference.png'));batches.append(dict(name=name,reference=f'front_batches/{name}_reference.png',items=items,slots=len(rows)))
    (out/'batches.json').write_text(json.dumps(batches,indent=2));print([(b['name'],[r['map'] for r in b['items']]) for b in batches])

if __name__=='__main__':main()
