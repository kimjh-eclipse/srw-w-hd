"""Reuse hd_parts_registration.registration_stamp between starts.

Kept OUT of hd_parts_registration.py on purpose: that file's bytes are part of every baked
texture key (hd_parts.registration_content), so editing it invalidates the whole
parts_baked.sqlite (107k textures; this happened for ten minutes on 2026-11-21).

The stamp reads every atlas of the approved parts (2,200+ files since the robot sets were
installed). With the parts library digest known, the last stamp is reused while that digest
and every file's size and modification time are unchanged; only file stats are read then.
Any cache problem falls back to the full computation.
"""
import json
from pathlib import Path
import tempfile

import hd_parts_registration
from hd_parts_registration import registration_stamp

FLAGS = ('auto_unit', 'auto_animation', 'auto_animation_reuse', 'auto_late_attack', 'auto_full_attack',
         'auto_shared_attack', 'observed_generated', 'observed_reuse', 'disabled')


def _cache_file():
    from runtime_paths import data_dir
    folder = data_dir() / 'cache'
    folder.mkdir(parents=True, exist_ok=True)
    return folder / 'registration-stamp.json'


def _stats(paths):
    out = []
    for path in paths:
        stat = Path(path).stat()
        out.append([stat.st_size, stat.st_mtime_ns])
    return out


def _paths(root, meta):
    """The files registration_stamp reads, in its order (same rule as that function)."""
    names = {b.get('atlas_id', 'base') for b in meta['bindings'] if not any(b.get(k) for k in FLAGS)}
    paths = [Path(hd_parts_registration.__file__), root / 'graphics/kazuma_parts_atlas_reference.png', root / 'graphics' / meta['atlas']]
    for name in sorted(names - {'base'}):
        extra = meta['atlases'][name]
        paths.extend([root / 'graphics' / extra['image'], root / 'graphics' / extra['reference']])
    return [str(path) for path in paths]


def cached_registration_stamp(root, meta, library_digest=None):
    if not library_digest:
        return registration_stamp(root, meta)
    try:
        target = _cache_file()
    except OSError:
        return registration_stamp(root, meta)
    try:
        saved = json.loads(target.read_text())
        if saved['library'] == library_digest and saved['root'] == str(root) and saved['stats'] == _stats(saved['paths']):
            return saved['stamp']
    except (OSError, ValueError, KeyError, TypeError):
        pass
    stamp = registration_stamp(root, meta)
    temporary = None
    try:
        names = _paths(root, meta)
        with tempfile.NamedTemporaryFile('w', dir=target.parent, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(dict(library=library_digest, root=str(root), paths=names, stats=_stats(names), stamp=stamp), stream, separators=(',', ':'))
        temporary.replace(target)
    except (OSError, KeyError):
        pass
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return stamp
