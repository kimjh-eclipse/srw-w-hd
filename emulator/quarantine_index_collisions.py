"""Exclude confirmed ambiguous identities from every indexed match table."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parent.parent
path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text())
report=json.loads((ROOT/'graphics/animation_parts/verification.json').read_text())
blocked=set(meta.get('indexed_collision_keys',[]))
for item in report.get('identity_errors',[]):blocked.add(meta['bindings'][item['binding']-1]['index_hash'])
meta['indexed_collision_keys']=sorted(blocked)
path.write_text(json.dumps(meta,indent=2));print('Ambiguous indexed identities excluded:',len(blocked))
