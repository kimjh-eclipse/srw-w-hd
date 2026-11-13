"""Build a separate, current-key-only texture store. Never replace the live DB."""
import argparse
import hashlib
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_parts import PartsRenderer


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.relative_to((ROOT / 'test_current').resolve())
    if output.exists():
        parser.error('Use a new candidate path; existing data is never overwritten.')
    output.parent.mkdir(parents=True, exist_ok=True)
    library = ROOT / 'graphics/kazuma_parts_library.json'
    before = hashlib.sha256(library.read_bytes()).hexdigest()
    renderer = PartsRenderer(async_prepare=False)
    try:
        source = renderer.disk_cache.path.resolve()
        wanted = set()
        for binding, spec in enumerate(renderer.bindings, 1):
            if spec.get('source_binding') or spec.get('runtime_texture') or spec.get('disabled'):
                continue
            wanted.add(renderer.texture_key(binding, spec['w'], spec['h']))
    finally:
        renderer.close()
    print(f'Current artwork keys: {len(wanted)}; copying existing blobs without encoding', flush=True)
    target = sqlite3.connect(output, uri=True)
    try:
        target.execute('ATTACH DATABASE ? AS original', (source.as_uri() + '?mode=ro',))
        target.execute('BEGIN')
        target.execute('CREATE TABLE textures (key TEXT PRIMARY KEY,w INTEGER,h INTEGER,pixels BLOB,stats TEXT)')
        target.execute('CREATE TEMP TABLE wanted (key TEXT PRIMARY KEY) WITHOUT ROWID')
        target.executemany('INSERT INTO wanted VALUES (?)', ((key,) for key in wanted))
        old_count = target.execute('SELECT count(*) FROM original.textures').fetchone()[0]
        expected = target.execute('SELECT count(*) FROM original.textures JOIN wanted USING(key)').fetchone()[0]
        target.execute('INSERT INTO textures SELECT s.* FROM original.textures s JOIN wanted USING(key)')
        count = target.execute('SELECT count(*) FROM textures').fetchone()[0]
        assert count == expected
        target.commit()
        print(f'Copied {count}/{old_count} existing rows; checking integrity and sample bytes', flush=True)
        assert target.execute('PRAGMA quick_check').fetchone()[0] == 'ok'
        keys = [row[0] for row in target.execute('SELECT key FROM textures ORDER BY key')]
        samples = keys[::max(1, len(keys) // 64)][:64]
        for key in samples:
            actual = target.execute('SELECT w,h,pixels,stats FROM textures WHERE key=?', (key,)).fetchone()
            original = target.execute('SELECT w,h,pixels,stats FROM original.textures WHERE key=?', (key,)).fetchone()
            assert actual == original, key
    finally:
        target.close()
    after = hashlib.sha256(library.read_bytes()).hexdigest()
    assert before == after, 'Library changed during copy; do not promote this candidate.'
    report = dict(source=str(source), candidate=str(output), library_sha256=before,
                  current_keys=len(wanted), source_rows=old_count, copied_rows=count,
                  discarded_stale_rows=old_count-count, source_bytes=source.stat().st_size,
                  candidate_bytes=output.stat().st_size, sample_blobs_identical=len(samples),
                  encoding_changed=False, source_replaced=False, library_unchanged=True)
    output.with_suffix('.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
