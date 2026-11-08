"""Read only display-sized menu pixels; retain the original art for editing."""
from pathlib import Path
from functools import lru_cache
import hashlib
import json
import sqlite3
import zlib
from PIL import Image

from asset_paths import asset_root
ROOT =asset_root(Path(__file__).resolve().parent.parent)
FOLDER = ROOT/'graphics/menu_units'
DATABASE = FOLDER/'display_sizes.sqlite'

@lru_cache(maxsize=64)
def _content_stamp(filename, modified, size):
    # One small compressed-file hash per asset/process; caches survive cloning
    # and copying, while edits invalidate them. No full-resolution PNG decode.
    return hashlib.sha256(Path(filename).read_bytes()).hexdigest()

def stamp(path):
    info = path.stat()
    return _content_stamp(str(path),info.st_mtime_ns,info.st_size)

def load_texture(filename, width, database=None):
    source = FOLDER/filename
    if database is not None:
        try:
            row = database.execute('SELECT w,h,pixels FROM textures WHERE name=? AND width=? AND stamp=?',
                                   (filename, width, stamp(source))).fetchone()
            if row:
                return Image.frombytes('RGBA', (row[0], row[1]), zlib.decompress(row[2])), True
        except (sqlite3.Error, ValueError, zlib.error):
            pass
    with Image.open(source) as image:
        art = image.convert('RGBA')
    basis=json.loads((FOLDER/'scene_runtime.json').read_text()).get('source_width',1440)
    if width != basis:
        art = art.resize((round(art.width*width/basis), round(art.height*width/basis)), Image.Resampling.LANCZOS)
    return art, False

def open_database():
    if not DATABASE.exists():
        return None
    try:
        return sqlite3.connect(DATABASE.as_uri()+'?mode=ro', uri=True, timeout=.05)
    except sqlite3.Error:
        return None
