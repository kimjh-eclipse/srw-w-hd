"""Freeze reviewed mechanical BG pictures; exclude corrupt or unclassified decodes."""
import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from PIL import Image

REVIEWED={22718,22721,22724,22727,22730,22745,22749,22752,22784,
22813,22828,22948,23010,23013,23036,23039,23054,23060,23076,
23099,23175,23232,23235,23238,23299,23317,23322,23353,23365,
23378,23442,23460,23463,23521,23530,23624,23630,23637,23999,
24101,24385,24388,24405,26695,28484}

def main():
    folder=ROOT/'graphics/mechanical_cutins';folder.mkdir(exist_ok=True)
    target=folder/'plan.json'
    if target.exists():print('Existing plan retained');return
    inventory=json.loads((ROOT/'test_current/parts/cutin_bank/inventory.json').read_text())['images']
    existing={p.get('resource') for p in json.loads((ROOT/'graphics/cutins_library.json').read_text())['cutins']}
    rows=[r for r in inventory if r['image'] in REVIEWED and r['image'] not in existing and not r.get('error')]
    assert {r['image'] for r in rows}|existing >= REVIEWED
    pairs=[]
    for at in range(0,len(rows),2):
        name=f'mechanical_pair_{at//2:02}';canvas=Image.new('RGBA',(256,512));items=[]
        for slot,row in enumerate(rows[at:at+2]):
            source=ROOT/f'test_current/parts/cutin_bank/bg_{row["image"]}_native.png'
            with Image.open(source) as im:canvas.paste(im.convert('RGBA').crop((0,0,256,256)),(0,slot*256))
            items.append(dict(**row,slot=slot,native_size=[256,256]))
        canvas.save(folder/(name+'_native.png'))
        canvas.resize((768,1536),Image.Resampling.NEAREST).save(folder/(name+'_reference.png'))
        pairs.append(dict(name=name,reference=name+'_reference.png',output=name+'_generated.png',items=items))
    target.write_text(json.dumps(dict(scope='Reviewed mechanical BG artwork; registration and gameplay validation required',pairs=pairs),indent=2))
    print('Mechanical resources',len(rows),'canvases',len(pairs))

if __name__=='__main__':main()
