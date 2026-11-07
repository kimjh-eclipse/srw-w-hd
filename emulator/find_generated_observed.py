from pathlib import Path
import time,json,shutil
from PIL import Image
import numpy as np
root=Path('.');out=root/'graphics/observed_parts';targets={p.stem.replace('_native',''):np.asarray(Image.open(p).getchannel('A'))>64 for p in out.glob('*_native.png')}
found={}
for p in Path('C:/Users/OXP2/.codex/generated_images/01a1ae5f-b72a-7381-9484-facc1f5556b3').glob('*.png'):
    if time.time()-p.stat().st_mtime>1800:continue
    im=Image.open(p)
    if im.mode!='RGBA':continue
    a=np.asarray(im.resize((256,256),Image.Resampling.LANCZOS).getchannel('A'))>64
    scores=[(float((a&b).sum()/max(1,(a|b).sum())),name) for name,b in targets.items()];score,name=max(scores)
    if score>.55 and (name not in found or score>found[name]['iou']):found[name]=dict(path=str(p),iou=score)
for name,record in found.items():shutil.copyfile(record['path'],out/f'{name}_hd.png')
(out/'discovered.json').write_text(json.dumps(found,indent=2));print(json.dumps(found,indent=2))
