"""Split the repaired joined face back into its original atlas parts.

Only RGB in the lower-face band is changed. Atlas alpha, coordinates, upper
helmet and every unrelated body part remain byte-identical to the base atlas.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json
import numpy as np
from PIL import Image

ROOT=PROJECT_ROOT
base=Image.open(ROOT/'graphics/kazuma_parts_atlas_hd.png').convert('RGBA').resize((2048,1024),Image.Resampling.LANCZOS)
paint=Image.open(ROOT/'graphics/kazuma_face_repaired.png').convert('RGBA').resize((320,320),Image.Resampling.LANCZOS)
result=np.array(base);before=result.copy();fixed=np.array(paint)
yy=np.arange(320);feather=np.minimum(np.clip((yy-200)/24,0,1),np.clip((312-yy)/16,0,1))
allowed=np.zeros(result.shape[:2],dtype=bool)
for source,target in [((0,0,256,256),(0,0)),((256,0,320,256),(256,0)),((16,256,272,320),(1792,0))]:
    sx,sy,ex,ey=source;tx,ty=target;h,w=ey-sy,ex-sx
    patch=fixed[sy:ey,sx:ex];weight=feather[sy:ey,None]*(patch[:,:,3]/255)
    old=result[ty:ty+h,tx:tx+w,:3]
    result[ty:ty+h,tx:tx+w,:3]=np.rint(old*(1-weight[:,:,None])+patch[:,:,:3]*weight[:,:,None]).astype('uint8')
    allowed[ty:ty+h,tx:tx+w]=weight>0
assert np.array_equal(result[:,:,3],before[:,:,3]),'part silhouette changed'
assert np.array_equal(result[~allowed],before[~allowed]),'unrelated atlas pixels changed'
Image.fromarray(result).save(ROOT/'graphics/kazuma_parts_atlas_facefix.png')
meta_path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(meta_path.read_text());meta['atlas']='kazuma_parts_atlas_facefix.png';meta_path.write_text(json.dumps(meta,indent=2))
report=dict(changed_rgb_pixels=int(np.any(result[:,:,:3]!=before[:,:,:3],axis=2).sum()),alpha_unchanged=True,non_face_pixels_unchanged=True)
(ROOT/'test_current/parts/face_patch_verification.json').write_text(json.dumps(report,indent=2));print(report)
