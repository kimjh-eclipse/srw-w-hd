"""Pack all archive portraits as numbered fixed-layout AI redraw sheets."""
import json
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/portraits';SHEETS=OUT/'sheets';SHEETS.mkdir(exist_ok=True)
def main():
    records=json.loads((OUT/'archive/catalog.json').read_text())['portraits']
    # Observed individual paintings take precedence over the archive batch.
    known={x['img'] for x in json.loads((OUT/'archive/observed_matches.json').read_text()) if x['error']==0}
    todo=[x for x in records if x['img'] not in known];plans=[]
    for start in range(0,len(todo),16):
        items=todo[start:start+16];n=start//16;im=Image.new('RGBA',(256,224))
        cells=[]
        for i,item in enumerate(items):
            x=i%4*64+4;y=i//4*56+4;source=Image.open(OUT/item['path']).convert('RGBA');im.paste(source,(x,y))
            cells.append(dict(**item,rectangle=[x,y,56,48]))
        name=f'portraits_{n:02}';im.save(SHEETS/(name+'_native.png'));im.resize((2048,1792),Image.Resampling.NEAREST).save(SHEETS/(name+'_reference.png'))
        plans.append(dict(name=name,native_size=[256,224],items=cells))
    (SHEETS/'plan.json').write_text(json.dumps(dict(sheets=plans,known=sorted(known),total=len(records)),indent=2));print(len(plans),len(todo))
if __name__=='__main__':main()
