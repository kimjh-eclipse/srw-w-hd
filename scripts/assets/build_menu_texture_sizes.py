"""Precompute the exact old Lanczos result at every supported menu resolution."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json
import os
import sqlite3
import time
import zlib
from PIL import Image
from menu_texture_cache import DATABASE,FOLDER,stamp
from render_resolution import MIN_WIDTH,MAX_WIDTH

def main():
    start = time.perf_counter()
    spec = json.loads((FOLDER/'scene_runtime.json').read_text())
    basis=spec.get('source_width',1440)
    temporary = DATABASE.with_suffix('.tmp.sqlite')
    if temporary.exists():
        temporary.unlink()
    count = 0
    with sqlite3.connect(temporary) as db:
        db.execute('CREATE TABLE textures(name TEXT,width INTEGER,stamp TEXT,w INTEGER,h INTEGER,pixels BLOB,PRIMARY KEY(name,width))')
        for name in spec['images'].values():
            source = FOLDER/name
            with Image.open(source) as opened:
                original = opened.convert('RGBA')
            for width in range(MIN_WIDTH,MAX_WIDTH+1,32):
                art = original if width==basis else original.resize(
                    (round(original.width*width/basis),round(original.height*width/basis)),Image.Resampling.LANCZOS)
                db.execute('INSERT INTO textures VALUES(?,?,?,?,?,?)',
                           (name,width,stamp(source),art.width,art.height,zlib.compress(art.tobytes(),3)))
                count += 1
    db.close()
    os.replace(temporary,DATABASE)
    print(json.dumps(dict(textures=count,bytes=DATABASE.stat().st_size,seconds=time.perf_counter()-start)))

if __name__=='__main__':
    main()
