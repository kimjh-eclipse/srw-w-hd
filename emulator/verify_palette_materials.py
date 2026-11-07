"""Verify runtime palette changes can split equal-colored source materials."""
import base64,zlib,json
from pathlib import Path
import numpy as np
from palette_materials import material_indices

native=np.ones((8,16),dtype='uint8');native[:,8:]=2
encoded=base64.b64encode(zlib.compress(native.tobytes())).decode('ascii')
source=np.array([[0,0,0],[128,128,128],[128,128,128],[255,255,255]],dtype='float32')
fallback=np.ones((80,160),dtype='uint8')
indices=material_indices(encoded,16,8,(160,80),fallback,source)
target=np.array([[0,0,0],[240,20,10],[10,30,240],[255,255,255]],dtype='uint8');actual=target[indices]
assert np.all(actual[:,:80]==[240,20,10]) and np.all(actual[:,80:]==[10,30,240])
# A separately painted highlight keeps its own color identity at the boundary.
fallback[:,78:82]=3;indices=material_indices(encoded,16,8,(160,80),fallback,source)
assert np.all(indices[:,78:82]==3)
report=dict(equal_source_colors_split_by_original_material=True,distinct_hd_highlight_preserved=True,actual_runtime_palette_used=True)
out=Path(__file__).resolve().parent.parent/'test_current/parts/palette_materials.json';out.write_text(json.dumps(report,indent=2));print(json.dumps(report))
