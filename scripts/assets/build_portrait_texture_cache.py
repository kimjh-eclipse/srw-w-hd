"""Bake final masked portrait textures; runtime needs only fast decompression."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,sqlite3,zlib
from pathlib import Path
from hd_portraits import ROOT,_prepare_art_from_source,_asset_stamp
library=json.loads((ROOT/'graphics/portraits/library.json').read_text())['portraits'];target=ROOT/'graphics/portraits/prepared.sqlite';temporary=target.with_suffix('.sqlite.tmp')
if temporary.exists():temporary.unlink()
database=sqlite3.connect(temporary);database.execute('CREATE TABLE art(path TEXT PRIMARY KEY,stamp TEXT,w INTEGER,h INTEGER,pixels BLOB)')
for item in library:
    art=_prepare_art_from_source(item);database.execute('INSERT INTO art VALUES(?,?,?,?,?)',(item['path'],_asset_stamp(item),art.width,art.height,zlib.compress(art.tobytes(),3)))
database.commit();database.close();temporary.replace(target);print(json.dumps(dict(textures=len(library),bytes=target.stat().st_size)))
