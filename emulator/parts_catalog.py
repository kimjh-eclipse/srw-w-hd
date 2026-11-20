"""Read the parts manifest shared by the core, compositor and texture worker.

The JSON pack is authoritative. Its digest also identifies the material tables.
A disposable local copy interns repeated RGB palettes to avoid allocating
millions of tiny lists on every process start. Renderers read palettes only.
"""
import hashlib
import json
from pathlib import Path
import tempfile
from zipfile import BadZipFile, ZipFile

from runtime_paths import data_dir


def _pack(library):
    palettes = []
    palette_ids = {}
    references = []
    rows = []
    for number, binding in enumerate(library['bindings']):
        row = binding.copy()
        for field in ('original_palette_rgb', 'palette_source_rgb', 'palette_rgb'):
            value = row.get(field)
            if not isinstance(value, list):
                continue
            key = json.dumps(value, separators=(',', ':'))
            index = palette_ids.get(key)
            if index is None:
                index = len(palettes)
                palettes.append(value)
                palette_ids[key] = index
            references.append((number, field, index))
            del row[field]
        rows.append(row)
    return [dict(library, bindings=rows), palettes, references]


def _unpack(packed):
    library, palettes, references = packed
    bindings = library['bindings']
    for number, field, index in references:
        bindings[number][field] = palettes[index]
    return library


def load_parts_library(source, cache_dir=None):
    # One replaceable entry per pack, even when a developer edits it repeatedly.
    pack_id = hashlib.sha256(str(source.resolve()).encode('utf-8')).hexdigest()[:24]
    try:
        folder = Path(cache_dir) if cache_dir is not None else data_dir() / 'cache'
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / ('part-catalog-' + pack_id + '.zip')
    except OSError:
        raw = source.read_bytes()
        return json.loads(raw), hashlib.sha256(raw).hexdigest()

    try:
        with ZipFile(path) as archive:
            # Check the actual pack even if a replacement preserved the timestamp.
            # Stream it so a cache hit doesn't hold the entire source in memory.
            checksum = hashlib.sha256()
            with source.open('rb') as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b''):
                    checksum.update(block)
            digest = checksum.hexdigest()
            packed = json.loads(archive.read('v1-' + digest))
        return _unpack(packed), digest
    except (OSError, BadZipFile, KeyError, ValueError, TypeError, IndexError, EOFError):
        pass

    raw = source.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    library = json.loads(raw)
    del raw
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=folder, suffix='.tmp', delete=False) as stream:
            temporary = Path(stream.name)
            with ZipFile(stream, 'w') as archive:
                archive.writestr('v1-' + digest, json.dumps(_pack(library), separators=(',', ':')).encode())
        temporary.replace(path)
    except OSError:
        pass  # A read-only or full cache still permits playing from the pack.
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return library, digest
