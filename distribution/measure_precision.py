from pathlib import Path
import io,json
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent

def main():
    report=json.loads((ROOT/'test_current/image_optimization/package_images.json').read_text());rows=[]
    for folder in ('animation_parts','map_tiles','scenario_backgrounds','all_units','battle_backgrounds','portraits','wing_parts','menu_units'):
        candidates=[r for r in report['entries'] if r['path'].startswith(folder+'/') and r.get('encoded')]
        row=max(candidates,key=lambda r:r['after']);a=np.array(Image.open(ROOT/row['encoded']).convert('RGBA'));rounded=a.copy();rounded[:,:,:3]=np.minimum(255,((a[:,:,:3].astype('uint16')+2)//4)*4).astype('uint8');stream=io.BytesIO();Image.fromarray(rounded).save(stream,'WEBP',lossless=True,quality=90,method=4,exact=True)
        result=dict(path=row['path'],before=row['after'],after=len(stream.getvalue()),ratio=round(len(stream.getvalue())/row['after'],3));rows.append(result);print(result,flush=True)
    (ROOT/'test_current/image_optimization/precision_measurements.json').write_text(json.dumps(rows,indent=2))

if __name__=='__main__':main()
