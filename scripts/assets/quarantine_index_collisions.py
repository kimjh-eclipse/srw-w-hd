"""Exclude confirmed ambiguous identities from every indexed match table."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json
ROOT=PROJECT_ROOT
path=ROOT/'graphics/kazuma_parts_library.json';meta=json.loads(path.read_text())
report=json.loads((ROOT/'graphics/animation_parts/verification.json').read_text())
blocked=set(meta.get('indexed_collision_keys',[]))
for item in report.get('identity_errors',[]):blocked.add(meta['bindings'][item['binding']-1]['index_hash'])
meta['indexed_collision_keys']=sorted(blocked)
path.write_text(json.dumps(meta,indent=2));print('Ambiguous indexed identities excluded:',len(blocked))
