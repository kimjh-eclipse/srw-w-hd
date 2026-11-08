"""Collect matching player/tool sources without local games or user data."""
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN = {'.dll', '.exe', '.state', '.nds', '.gba', '.iso', '.rom', '.sav',
             '.dsv', '.srm', '.bin', '.log', '.npz', '.npy', '.json', '.png',
             '.webp', '.wav', '.pcm', '.pyc', '.key', '.pem'}
METADATA = {'scripts/tool_index.json', 'docs/source_moves.json'}


def source_candidates():
    tracked = subprocess.check_output(
        ['git', 'ls-files', '-z', 'emulator', 'distribution', 'scripts', 'docs',
         'REPOSITORY.md', 'README.md', 'run.py'], cwd=ROOT).decode().split('\0')
    candidates = {name for name in tracked if name}
    # Include new/moved first-party files even before they have been staged.
    for directory in ('scripts', 'docs', 'distribution'):
        candidates.update(p.relative_to(ROOT).as_posix() for p in (ROOT/directory).rglob('*')
                          if p.is_file() and '__pycache__' not in p.parts)
    candidates.update(p.relative_to(ROOT).as_posix() for p in (ROOT/'emulator').glob('*.py'))
    candidates.add('run.py')
    return sorted(name for name in candidates if (ROOT/name).is_file()
                  and (name in METADATA or (ROOT/name).suffix.lower() not in FORBIDDEN)
                  and Path(name).name != 'player_settings.json')


def write_source_bundle(destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    names = source_candidates()
    with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as archive:
        for name in names:
            archive.write(ROOT/name, name)
    return names
