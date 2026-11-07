"""Locate archive face placement against exact observed native battle crops."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'graphics/portraits'
def main():
    records=json.loads((OUT/'archive/catalog.json').read_text())['portraits'];matches=[]
    for plan in ('observed.json','observed_extra.json'):
        for portrait in json.loads((OUT/plan).read_text())['portraits']:
            native=np.asarray(Image.open(OUT/(portrait['name']+'_native.png')).convert('RGB'))
            target=native[2:46,5:48]>>3;best=(1e9,None)
            for record in records:
                raw=np.asarray(Image.open(OUT/record['path']).convert('RGBA'))
                for dy in range(-2,3):
                    for dx in range(0,9):
                        sy=2-dy;sx=5-dx
                        if sy<0 or sx<0 or sy+44>48 or sx+43>56:continue
                        sample=raw[sy:sy+44,sx:sx+43]
                        error=np.abs((sample[:,:,:3]>>3).astype('int16')-target).mean()
                        if error<best[0]:best=(float(error),dict(img=record['img'],dx=dx,dy=dy))
            matches.append(dict(name=portrait['name'],error=best[0],**best[1]));print(matches[-1],flush=True)
    (OUT/'archive/observed_matches.json').write_text(json.dumps(matches,indent=2))
if __name__=='__main__':main()
