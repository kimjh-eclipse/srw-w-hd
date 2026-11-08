"""Keep prepared textures valid after a verified pixel-identical recompression."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import hashlib
import json
import os
from pathlib import Path
import sqlite3
import numpy as np
from hd_parts_registration import registration_stamp

ROOT = PROJECT_ROOT

def retag(report):
    if not report['pixel_exact'] or report['errors']:
        raise ValueError('Cannot migrate caches without successful pixel verification')
    entries = {r['path']: r for r in report['entries'] if r['status']=='optimized'}
    meta = json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
    version = hashlib.sha256((ROOT/'emulator/hd_parts_registration.py').read_bytes()).hexdigest()
    keys = set()
    database = ROOT/'graphics/parts_registered.sqlite'
    moved = 0
    with sqlite3.connect(database) as db:
        for source in meta['bindings']:
            spec = meta.get('atlases', {}).get(source.get('atlas_id', 'base'),
                dict(image='kazuma_parts_atlas_facefix.png', reference='kazuma_parts_atlas_reference.png'))
            original = [version, 'native-crop-v2', source['x'], source['y'], source['w'], source['h']]
            current = original.copy()
            for name in (spec['image'], spec['reference']):
                path = ROOT/'graphics'/name
                stat = path.stat()
                old = entries.get(path.relative_to(ROOT).as_posix())
                original.extend([str(path), stat.st_mtime_ns, old['before'] if old else stat.st_size])
                current.extend([str(path), stat.st_mtime_ns, stat.st_size])
            oldkey = hashlib.sha256(json.dumps(original).encode()).hexdigest()
            newkey = hashlib.sha256(json.dumps(current).encode()).hexdigest()
            if oldkey != newkey and oldkey not in keys:
                keys.add(oldkey)
                moved += db.execute('UPDATE OR IGNORE parts SET key=? WHERE key=?', (newkey,oldkey)).rowcount
    target = ROOT/'graphics'/meta.get('registration_cache', 'kazuma_parts_registration.npz')
    with np.load(target, allow_pickle=False) as archive:
        arrays = {name: archive[name] for name in archive.files}
    arrays['stamp'] = np.array(registration_stamp(ROOT, meta))
    temporary = target.with_suffix('.tmp.npz')
    np.savez_compressed(temporary, **arrays)
    os.replace(temporary, target)
    return dict(part_cache_keys_migrated=moved, approved_cache_retagged=True)

if __name__ == '__main__':
    path = ROOT/'test_current/image_optimization/report.json'
    report = json.loads(path.read_text(encoding='utf-8'))
    print(json.dumps(retag(report)))
