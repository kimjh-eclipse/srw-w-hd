"""Audit selected installed batches without overwriting the full-ROM audit."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.verify import audit_all_parts as quality
from scripts.verify import audit_palette_alignment as palette


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reports', type=Path, nargs='*', default=[])
    parser.add_argument('--bindings', type=int, nargs='*', default=[])
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.relative_to((ROOT / 'test_current').resolve())
    output.mkdir(parents=True, exist_ok=True)
    ids = set(args.bindings)
    sources = {}
    for path in args.reports:
        report = json.loads(path.read_text(encoding='utf-8'))
        if not report.get('applied'):
            parser.error(f'Batch was not installed: {path}')
        values = sorted({int(row['binding']) for row in report['parts']})
        ids.update(values)
        sources[str(path)] = values
    if not ids:
        parser.error('Select installed bindings or batch reports.')
    library = ROOT / 'graphics/kazuma_parts_library.json'
    digest = lambda: hashlib.sha256(library.read_bytes()).hexdigest()
    before = digest()
    results = {}
    errors = []
    missing_baked = []
    for module, name in ((palette, 'palette_alignment'), (quality, 'quality_audit')):
        module.start()
        rows = []
        try:
            if name == 'quality_audit':
                renderer = module._renderer
                keys = renderer.disk_cache.keys()
                for binding in sorted(ids):
                    spec = renderer.bindings[binding - 1]
                    if renderer.texture_key(binding, spec['w'], spec['h']) not in keys:
                        missing_baked.append(binding)
            for binding in sorted(ids):
                try:
                    rows.append(module.analyse(binding) or dict(binding=binding, skipped=True))
                except Exception as error:
                    errors.append(dict(check=name, binding=binding, error=str(error)))
        finally:
            module._renderer.close()
        results[name] = rows
        (output / f'{name}.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
    after = digest()
    p, q = results['palette_alignment'], results['quality_audit']
    summary = dict(
        scope='Selected installed artwork only. Metrics screen for review; actual replay and human visual review are separate.',
        bindings=sorted(ids), installed_parts=len(ids), source_reports=sources,
        library_sha256_before=before, library_sha256_after=after, library_unchanged=before == after,
        missing_baked=missing_baked,
        palette_measured=sum('wrong_colour_share' in row for row in p),
        palette_rule_failures=[row for row in p if row.get('wrong_colour_share', 0) >= .02 or row.get('slots_never_native')],
        quality_measured=sum('flags' in row for row in q),
        quality_flagged=[row for row in q if row.get('flags')], errors=errors,
        all_units_complete=False, gameplay_verified_by_this_audit=False)
    (output / 'summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
    print(json.dumps(dict(installed_parts=len(ids), missing_baked=missing_baked,
                         palette_failures=len(summary['palette_rule_failures']),
                         quality_flags=[(row['binding'], row['flags']) for row in summary['quality_flagged']],
                         errors=errors, library_unchanged=before == after)))
    if errors or missing_baked or before != after:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
