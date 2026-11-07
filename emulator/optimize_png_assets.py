"""Lossless PNG recompression with pixel verification and atomic replacement.

The approved face atlas is deliberately immutable. Never quantizes, resizes,
changes alpha, or replaces a file unless decoded mode/size/bytes match exactly.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PROTECTED = {'kazuma_parts_atlas_facefix.png'}

def identity(path):
    with Image.open(path) as im:
        return im.mode, im.size, hashlib.sha256(im.tobytes()).hexdigest()

def optimize(path, executable):
    before = path.stat()
    row = dict(path=path.relative_to(ROOT).as_posix(), before=before.st_size,
               after=before.st_size, status='unchanged')
    if path.name in PROTECTED:
        row['status'] = 'protected'
        return row
    original = identity(path)
    fd, temporary = tempfile.mkstemp(suffix='.png', dir=path.parent)
    os.close(fd)
    try:
        result = subprocess.run([str(executable), '-o', '2', '--nx', '--threads', '1',
                                 '--out', temporary, str(path)], capture_output=True)
        if result.returncode:
            raise RuntimeError(result.stderr.decode(errors='replace')[-500:])
        if identity(temporary) != original:
            raise ValueError('decoded image changed; original retained')
        row['pixel_sha256'] = original[2]
        size = os.path.getsize(temporary)
        if size < before.st_size:
            os.utime(temporary, ns=(before.st_atime_ns, before.st_mtime_ns))
            os.replace(temporary, path)
            row.update(after=size, status='optimized')
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return row

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--workers', type=int, default=4)
    args = parser.parse_args()
    executable = next((ROOT/'tools/oxipng').rglob('oxipng.exe'))
    target = ROOT/'test_current/image_optimization'
    target.mkdir(parents=True, exist_ok=True)
    # Recompression changes file sizes. Retag only caches that were valid before
    # this run, after verifying every source pixel remained identical.
    import hd_portraits
    library = json.loads((ROOT/'graphics/portraits/library.json').read_text())['portraits']
    old_stamps = {item['path']: hd_portraits._asset_stamp(item) for item in library}
    files = sorted((ROOT/'graphics').rglob('*.png'))
    rows = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        tasks = {pool.submit(optimize, p, executable): p for p in files}
        for future in as_completed(tasks):
            path = tasks[future]
            try:
                rows.append(future.result())
            except Exception as exc:
                rows.append(dict(path=path.relative_to(ROOT).as_posix(), status='error', error=str(exc)))
            if len(rows) % 200 == 0:
                print(json.dumps(dict(done=len(rows), total=len(files), saved_bytes=sum(
                    r.get('before', 0)-r.get('after', 0) for r in rows))), flush=True)
    errors = [r for r in rows if r['status']=='error']
    if not errors:
        cache = ROOT/'graphics/portraits/prepared.sqlite'
        if cache.exists():
            with sqlite3.connect(cache) as db:
                for item in library:
                    db.execute('UPDATE art SET stamp=? WHERE path=? AND stamp=?',
                               (hd_portraits._asset_stamp(item), item['path'], old_stamps[item['path']]))
    report = dict(files=len(files), optimized=sum(r['status']=='optimized' for r in rows),
                  before=sum(r.get('before',0) for r in rows), after=sum(r.get('after',0) for r in rows),
                  errors=errors, pixel_exact=not errors, entries=rows)
    (target/'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if not errors:
        from retag_lossless_asset_caches import retag
        migration = retag(report)
        (target/'cache_migration.json').write_text(json.dumps(migration, indent=2), encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='entries'}), flush=True)
    return bool(errors)

if __name__ == '__main__':
    raise SystemExit(main())
