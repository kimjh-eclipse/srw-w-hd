"""List or run development tools from any working directory."""
from pathlib import Path
import argparse
import json
import runpy
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts._bootstrap import ROOT, tool_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('tool', nargs='?', help='Tool filename without .py')
    parser.add_argument('--list', action='store_true', help='List tools grouped by purpose')
    args, remaining = parser.parse_known_args()
    index = json.loads((ROOT/'scripts/tool_index.json').read_text(encoding='utf-8'))
    if args.list or not args.tool:
        for group in ('assets', 'build', 'diagnostics', 'verify'):
            print(group + ':')
            for name, path in index.items():
                if path.startswith('scripts/'+group+'/'): print('  '+name)
        return
    target = tool_path(args.tool)
    sys.argv = [str(target), *remaining]
    runpy.run_path(str(target), run_name='__main__')


if __name__ == '__main__': main()
