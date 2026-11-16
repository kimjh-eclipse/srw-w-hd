"""Disable 8x8 bindings whose native tile is a single opaque colour.

A flat tile has nothing to redraw, and its RGB key also matches plain tiles in
unrelated scenes (unit 338 frame 240: a white BG1 tile behind the robot sprites
was painted over the HD robot as a white box).

  py -3.11 -X utf8 scripts/assets/disable_flat_tiles.py
"""
import base64,json,sys,zlib
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
LIB=ROOT/'graphics/kazuma_parts_library.json'
lib=json.loads(LIB.read_text(encoding='utf-8'));n=[]
for i,b in enumerate(lib['bindings'],1):
    if b.get('w')!=8 or b.get('h')!=8 or b.get('disabled') or not b.get('index_pixels'):continue
    try:ix=np.frombuffer(zlib.decompress(base64.b64decode(b['index_pixels'])),dtype='uint8')
    except Exception:continue
    u=np.unique(ix)
    if len(u)==1 and u[0]!=0:b['disabled']=True;b['disabled_reason']='flat single-colour 8x8 tile: nothing to redraw, key collides with plain tiles';n.append(i)
LIB.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8');print('disabled',n)
