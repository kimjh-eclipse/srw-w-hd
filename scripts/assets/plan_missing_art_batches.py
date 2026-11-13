"""Prioritize old missing-art contracts against current production bindings.

This is a production queue, not a new ROM audit or a visual-quality verdict.
The old report omits multi-image patterns and runtime-only palette variants.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, default=ROOT/'test_current/parts/missing_export/report.json')
    parser.add_argument('--output', type=Path, default=ROOT/'test_current/parts/missing_production_queue/current.json')
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding='utf-8'))
    meta = json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))
    exact, indexed = set(), set()
    for part in meta['bindings']:
        if part.get('disabled'):
            continue
        size = part.get('w'), part.get('h')
        if part.get('rgb_enabled', True):
            exact.add((part.get('hash'), *size))
        if part.get('indexed_safe', True):
            indexed.add((part.get('index_hash'), *size))
    batches = []
    for image in report['images']:
        pending = []
        for part in image['missing']:
            size = part['w'], part['h']
            if (part['hash'], *size) in exact or (part['index_hash'], *size) in indexed:
                continue
            pending.append(part)
        if not pending:
            continue
        batches.append(dict(image=image['image'], palette=image.get('palette'),
                            pattern=image.get('pattern'), units=image.get('units', []),
                            in_test_window=image.get('in_test_window', False),
                            seen_frames=sum((p.get('seen') or {}).get('frames', 0) for p in pending),
                            pending_contracts=len(pending),
                            pending_opaque=sum(p.get('opaque', 0) for p in pending),
                            source_sheet=f"test_current/parts/missing_export/image_{image['image']:05d}.png",
                            parts=pending))
    batches.sort(key=lambda b: (b['seen_frames'] > 0, b['in_test_window'],
                                b['seen_frames'], b['pending_opaque']), reverse=True)
    output = dict(kind='production_selection_only_not_total_remaining',
                  old_report_distinct_missing=report.get('distinct_missing'),
                  limitations=['No new ROM enumeration or visual review.',
                               'Old contracts may use unobserved palettes: confirm before painting.',
                               'Runtime-only and multi-image omissions are not counted here.',
                               'A registered binding does not prove that its artwork is correct.'],
                  candidate_images=len(batches), batches=batches)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2), encoding='utf-8')
    print(json.dumps(dict(candidate_images=len(batches), top=[
        {k: row[k] for k in ('image', 'pending_contracts', 'seen_frames')}
        for row in batches[:12]])))


if __name__ == '__main__':
    main()
