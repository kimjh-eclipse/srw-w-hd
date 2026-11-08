"""One-time, checked source relocation. Existing artwork and player data stay put."""
from pathlib import Path
import ast, collections, hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[2]
KEEP_DIRS = {'emulator', 'graphics', 'distribution', 'test_current', 'tools',
             'build', 'dist', 'inputs', 'baseline', 'release_battle_v02',
             'release', 'reference_bgm', '.git', '__pycache__', 'research', 'scripts', 'docs'}
KEEP_FILES = {'AGENTS.md', 'README.md', 'REPOSITORY.md', '.gitignore', '.gitattributes'}
RUNTIME_EXTRA = {'hd_robot', 'sdl_pad_state'}


def group(name):
    if name.startswith('verify_'): return 'verify'
    if name.startswith('build_native_') or name == 'export_core_patch': return 'build'
    if name.startswith(('capture_', 'inspect_', 'find_', 'locate_', 'probe_',
                        'profile_', 'benchmark_', 'diagnose_', 'preview_')) or name in {
                            'wing_gameplay_probe', 'persistent_pbo_prototype', 'summarize_hitch_measurements'}:
        return 'diagnostics'
    return 'assets'


files = {p.stem: p for p in (ROOT/'emulator').glob('*.py')}
deps = {}
for name, p in files.items():
    imports = set()
    for n in ast.walk(ast.parse(p.read_text(encoding='utf-8-sig'))):
        if isinstance(n, ast.Import): imports.update(a.name.split('.')[0] for a in n.names)
        if isinstance(n, ast.ImportFrom) and n.module: imports.add(n.module.split('.')[0])
    deps[name] = imports & files.keys()
runtime = set(RUNTIME_EXTRA)
pending = ['hd_emulator', 'hd_player', 'portable_entry', 'portable_selftest',
           'hd_parts_registration', 'tile_compositor', 'tile_group_paint']
while pending:
    name = pending.pop()
    if name in runtime or name.startswith('verify_'): continue
    runtime.add(name); pending.extend(deps.get(name, ()))

moves = {}
for name, p in files.items():
    if name not in runtime:
        moves[p.relative_to(ROOT).as_posix()] = f'scripts/{group(name)}/{p.name}'
moves['srw_graphics.py'] = 'scripts/assets/srw_graphics.py'
for p in ROOT.iterdir():
    if p.is_dir() and p.name not in KEEP_DIRS:
        moves[p.name] = f'research/legacy/{p.name}'
    elif p.is_file() and p.name not in KEEP_FILES and p.name not in moves:
        moves[p.name] = ('docs/' if p.name.endswith('.md') else 'research/legacy/') + p.name

ordered = sorted(moves, key=len, reverse=True)


def relocated(name):
    for old in ordered:
        if name == old or name.startswith(old+'/'):
            return moves[old] + name[len(old):]
    return name


module_moves = {Path(old).stem: new[:-3].replace('/', '.')
                for old, new in moves.items() if old.endswith('.py') and old.count('/') <= 1}


def fix_literal(value):
    # Keep git-show historical paths valid; those are rewritten separately below.
    if not isinstance(value, str) or ':' in value[:40]: return value
    if value.startswith('/'):
        return '/' + relocated(value[1:])
    return relocated(value)


def rewrite(path, text):
    old = path.relative_to(ROOT).as_posix()
    tree = ast.parse(text)
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines: offsets.append(offsets[-1] + len(line))
    edits = []
    for node in ast.walk(tree):
        replacement = None
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module in module_moves:
            replacement = 'from '+module_moves[node.module]+' import '+', '.join(
                a.name + (' as '+a.asname if a.asname else '') for a in node.names)
        elif isinstance(node, ast.Import) and any(a.name in module_moves for a in node.names):
            parts = []
            for a in node.names:
                if a.name not in module_moves:
                    parts.append('import '+a.name+(' as '+a.asname if a.asname else ''))
                elif a.asname:
                    parts.append('import '+module_moves[a.name]+' as '+a.asname)
                else:
                    package, name = module_moves[a.name].rsplit('.', 1)
                    parts.append('from '+package+' import '+name)
            replacement = '; '.join(parts)
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = fix_literal(node.value)
            if value != node.value: replacement = repr(value)
        if replacement is not None:
            # AST columns are UTF-8 bytes; convert to character offsets.
            begin = offsets[node.lineno-1]+len(lines[node.lineno-1].encode('utf-8')[:node.col_offset].decode('utf-8'))
            end = offsets[node.end_lineno-1]+len(lines[node.end_lineno-1].encode('utf-8')[:node.end_col_offset].decode('utf-8'))
            edits.append((begin, end, replacement))
    for begin, end, replacement in sorted(edits, reverse=True):
        text = text[:begin]+replacement+text[end:]
    if old in moves and moves[old].startswith('scripts/'):
        # These expressions used to point from emulator/ to the repository root.
        text = text.replace('Path(__file__).resolve().parent.parent', 'PROJECT_ROOT')
        if old == 'srw_graphics.py':
            text = text.replace('Path(__file__).resolve().parent', 'PROJECT_ROOT')
        else:
            text = text.replace('Path(__file__).resolve().parent', "(PROJECT_ROOT/'emulator')")
        tree = ast.parse(text); at = 0
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str):
            at = tree.body[0].end_lineno
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module == '__future__': at = node.end_lineno
        lines = text.splitlines(keepends=True)
        lines.insert(at, '\nimport sys as _sys\nfrom pathlib import Path as _Path\n'
                     '_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))\n'
                     'from scripts._bootstrap import ROOT as PROJECT_ROOT\n\n')
        text = ''.join(lines)
    elif old in moves and old.endswith('.py') and '/' not in old:
        text = text.replace('Path(__file__).resolve().parent', 'PROJECT_ROOT')
        tree = ast.parse(text); at = 0
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant) and isinstance(tree.body[0].value.value, str): at = tree.body[0].end_lineno
        lines = text.splitlines(keepends=True)
        lines.insert(at, '\nimport sys as _sys\nfrom pathlib import Path as _Path\n'
                     '_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))\n'
                     'from scripts._bootstrap import ROOT as PROJECT_ROOT\n\n')
        text = ''.join(lines)
    # Historical git paths contain a colon and intentionally stay unchanged.
    ast.parse(text)
    return text


def main():
    # Check every final absolute target before moving any directory on Windows.
    for old, new in moves.items():
        source = (ROOT/old).resolve(); target = (ROOT/new).resolve()
        assert source.is_relative_to(ROOT) and target.is_relative_to(ROOT), (source, target)
        assert not target.exists(), target
    report = dict(runtime_modules=sorted(runtime), moves=moves,
                  moved_tools=sum(new.startswith('scripts/') for new in moves.values()),
                  root_directories_before=sum(p.is_dir() for p in ROOT.iterdir()),
                  root_files_before=sum(p.is_file() for p in ROOT.iterdir()))
    (ROOT/'test_current/layout/move_plan.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    if '--apply' not in sys.argv:
        print(json.dumps({k: v for k, v in report.items() if k not in ('moves','runtime_modules')})); return
    targets = list((ROOT/'emulator').glob('*.py'))+list((ROOT/'distribution').glob('*.py'))+list(ROOT.glob('*.py'))
    changed = []
    for p in targets:
        original = p.read_text(encoding='utf-8-sig'); updated = rewrite(p, original)
        if updated != original:
            p.write_text(updated, encoding='utf-8'); changed.append(p.relative_to(ROOT).as_posix())
    attributes = ROOT/'.gitattributes'
    attrs = attributes.read_text(encoding='utf-8')
    attrs = re.sub(r'"/([^"\n]+)"', lambda m: '"/'+relocated(m[1])+'"', attrs)
    attributes.write_text(attrs, encoding='utf-8')
    for old, new in moves.items():
        target = ROOT/new; target.parent.mkdir(parents=True, exist_ok=True)
        (ROOT/old).rename(target)
    for group_name in ('assets', 'build', 'diagnostics', 'verify'):
        p=ROOT/'scripts'/group_name; p.mkdir(parents=True, exist_ok=True)
        (p/'__init__.py').write_text('"""'+group_name+' development tools."""\n', encoding='utf-8')
    (ROOT/'scripts/__init__.py').write_text('"""Development tools; not player runtime modules."""\n', encoding='utf-8')
    report['rewritten_python_files'] = changed
    report['root_directories_after'] = sum(p.is_dir() for p in ROOT.iterdir())
    report['root_files_after'] = sum(p.is_file() for p in ROOT.iterdir())
    (ROOT/'test_current/layout/move_plan.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({k: v for k, v in report.items() if k not in ('moves','runtime_modules','rewritten_python_files')}))


if __name__ == '__main__': main()
