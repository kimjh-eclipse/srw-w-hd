"""Pack immutable original portrait references for one read per process."""
import json
from pathlib import Path
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parent.parent
library=json.loads((ROOT/'graphics/portraits/library.json').read_text())['portraits'];paths=sorted({x['portrait_mask'] for x in library if x.get('portrait_mask')})
rgba=np.stack([np.asarray(Image.open(ROOT/'graphics'/p).convert('RGBA')) for p in paths]);target=ROOT/'graphics/portraits/native_reference.npz';tmp=target.with_suffix('.npz.tmp')
with tmp.open('wb') as stream:np.savez_compressed(stream,paths=np.array(paths),rgba=rgba)
tmp.replace(target);print(len(paths),target.stat().st_size)
