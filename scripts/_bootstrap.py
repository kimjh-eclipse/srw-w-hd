"""Shared repository paths for directly executable development tools."""
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent.parent
for directory in (ROOT, ROOT/'emulator'):
    if str(directory) not in sys.path:
        sys.path.insert(0, str(directory))


def tool_path(name):
    """Resolve a development tool without assuming it lives next to the player."""
    name = Path(name).stem
    index = json.loads((ROOT/'scripts/tool_index.json').read_text(encoding='utf-8'))
    if name in index:
        return ROOT/index[name]
    runtime = ROOT/'emulator'/(name+'.py')
    if runtime.is_file():
        return runtime
    raise FileNotFoundError(f'Unknown project tool: {name}')
