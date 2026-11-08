"""Freeze two-cut-in restoration canvases from decoded native BG pictures."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import json
from PIL import Image

def main():
    folder=ROOT/'graphics/pilot_cutins';folder.mkdir(exist_ok=True)
    target=folder/'plan.json'
    if target.exists():print('Existing plan retained');return
    inv=json.loads((ROOT/'test_current/parts/cutin_bank/inventory.json').read_text())['images']
    old=json.loads((ROOT/'graphics/cutins_library.json').read_text())['cutins'];existing={p.get('resource') for p in old}|{24918}
    extras={22712,22715,22733,22742,22787,22805,22818,22822,22825,22839,22864,22867,22870,22873,22923,22945,22960,
            23050,23057,23152,23216,23241,23276,23279,23285,23499,23502,23505,23508,23511,23514,23518,
            23974,23977,23980,24391}
    rows=[p for p in inv if (24859<=p['image']<=25093 or 25652<=p['image']<=25668 or p['image'] in extras) and p['image'] not in existing and not p.get('error')]
    pairs=[]
    for at in range(0,len(rows),2):
        name=f'pilot_pair_{at//2:02}';native=Image.new('RGBA',(256,512));items=[]
        for slot,row in enumerate(rows[at:at+2]):
            source=ROOT/f'test_current/parts/cutin_bank/bg_{row["image"]}_native.png'
            with Image.open(source) as im:
                cropped=im.convert('RGBA').crop((0,0,min(256,im.width),min(256,im.height)))
                native.paste(cropped,(0,slot*256))
            items.append(dict(**row,slot=slot,native_size=[256,256]))
        native.save(folder/(name+'_native.png'));native.resize((768,1536),Image.Resampling.NEAREST).save(folder/(name+'_reference.png'))
        pairs.append(dict(name=name,reference=name+'_reference.png',output=name+'_generated.png',items=items))
    target.write_text(json.dumps(dict(scope='Visually reviewed pilot/body/eye BG pictures, excluding already approved cut-ins',pairs=pairs),indent=2))
    print('cutins',len(rows),'pairs',len(pairs))

if __name__=='__main__':main()
