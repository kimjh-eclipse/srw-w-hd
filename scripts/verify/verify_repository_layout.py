"""Check moved files, tool imports, reproducible source bundles and protected data."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT, tool_path

import ast
import hashlib
import importlib
import json
import subprocess
import zipfile
from distribution.source_bundle import FORBIDDEN, METADATA, write_source_bundle


def main():
    moves = json.loads((ROOT/'docs/source_moves.json').read_text(encoding='utf-8'))
    index = json.loads((ROOT/'scripts/tool_index.json').read_text(encoding='utf-8'))
    for old, new in moves.items():
        assert not (ROOT/old).exists(), old
        assert (ROOT/new).exists(), new
    for name, relative in index.items():
        path = tool_path(name)
        assert path == ROOT/relative and path.is_file(), name
    compiled = 0
    for directory in ('emulator', 'scripts', 'distribution'):
        paths = (ROOT/directory).glob('*.py') if directory == 'emulator' else (ROOT/directory).rglob('*.py')
        for path in paths:
            tree = ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
            compiled += 1
            for node in ast.walk(tree):
                modules = [a.name for a in node.names] if isinstance(node, ast.Import) else [node.module] if isinstance(node, ast.ImportFrom) else []
                for module in modules:
                    if module and module.startswith('scripts.'):
                        target = ROOT/Path(*module.split('.'))
                        assert target.with_suffix('.py').is_file() or (target/'__init__.py').is_file(), (path, module)
                if isinstance(node, ast.Constant) and isinstance(node.value, str):
                    value = node.value
                    if value.startswith('emulator/') and value.endswith('.py'):
                        assert (ROOT/value).is_file(), (path, value)
    plan = json.loads((ROOT/'test_current/layout/move_plan.json').read_text(encoding='utf-8'))
    for name in plan['runtime_modules']:
        importlib.import_module(name)
    # Git still reports old unstaged paths: each must have a corresponding file.
    tracked = subprocess.check_output(['git', 'ls-files', '-z'], cwd=ROOT).decode().split('\0')
    checked = 0
    for name in tracked:
        for old, new in sorted(moves.items(), key=lambda item: len(item[0]), reverse=True):
            if name == old or name.startswith(old+'/'):
                assert (ROOT/(new+name[len(old):])).exists(), name
                checked += 1
                break
    out = ROOT/'test_current/layout'
    archive_path = out/'source.zip'
    names = write_source_bundle(archive_path)
    required = {'run.py', 'scripts/_bootstrap.py', 'scripts/tool_index.json',
                'scripts/assets/srw_graphics.py', 'scripts/assets/build_text_patterns.py',
                'scripts/verify/verify_repository_layout.py', 'docs/SOURCE_LAYOUT.md',
                'docs/source_moves.json', 'emulator/hd_emulator.py',
                'emulator/desmume/desmume/COPYING'}
    assert required <= set(names), required-set(names)
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.testzip() is None
        assert all(name in METADATA or Path(name).suffix.lower() not in FORBIDDEN for name in archive.namelist())
        for name in required:
            assert archive.read(name) == (ROOT/name).read_bytes(), name
    for relative, digest in {
        'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds': '0a5a22bd6bb25ebe640767e6b422b91358636e9ae1300e61d7e8ac3c5d8cd478',
        'graphics/kazuma_parts_atlas_facefix.png': 'fc876ea3a755726ea8a2badfd9c44101f5a5410edf58f154625fd08cd9e897fe',
    }.items():
        with (ROOT/relative).open('rb') as source:
            assert hashlib.file_digest(source, 'sha256').hexdigest() == digest, relative
    result = dict(relocation_targets=len(moves),tracked_relocated_files_found=checked,
                  indexed_tools=len(index),parsed_python_files=compiled,
                  imported_runtime_modules=len(plan['runtime_modules']),source_bundle_files=len(names),
                  source_bundle_crc=True,protected_rom_and_face_unchanged=True,
                  private_files_in_source_bundle=False)
    (out/'verification.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__': main()
