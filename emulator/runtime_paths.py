"""Writable player data stays outside the bundled interpreter and HD artwork."""
from pathlib import Path
import os,sys,tempfile

FROZEN=bool(getattr(sys,'frozen',False))
APP_DIR=Path(sys.executable).resolve().parent if FROZEN else Path(__file__).resolve().parent.parent
_data=None

def data_dir():
    global _data
    if _data is None:
        candidate=APP_DIR/'data' if FROZEN and (APP_DIR/'portable.txt').exists() else Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'SRW_W_HD'
        try:
            candidate.mkdir(parents=True,exist_ok=True)
            with tempfile.TemporaryFile(dir=candidate):pass
        except OSError:
            candidate=Path(os.environ.get('LOCALAPPDATA',str(Path.home())))/'SRW_W_HD';candidate.mkdir(parents=True,exist_ok=True)
        _data=candidate
    return _data

def log_path(name):
    if not FROZEN:return Path(__file__).with_name(name)
    folder=data_dir()/'logs';folder.mkdir(exist_ok=True);return folder/name

def texture_cache(default):
    if not FROZEN:return default
    workspace=os.environ.get('SRWW_TEST_WORKSPACE')
    if workspace:
        prepared=Path(workspace)/'graphics'/Path(default).name
        if prepared.is_file():return prepared
    folder=data_dir()/'cache';folder.mkdir(exist_ok=True);return folder/Path(default).name

def shipped_texture_store(default,writable):
    """Finished textures delivered with a release, read only; None in a source checkout.

    The player's own store stays in data/cache (texture_cache) so an update can replace the
    delivered file. SRWW_SHIPPED_BAKED names a delivered store for tests.
    """
    named=os.environ.get('SRWW_SHIPPED_BAKED')
    if named:candidate=Path(named)
    elif FROZEN:candidate=Path(default)
    else:return None
    try:
        if candidate.is_file() and candidate.resolve()!=Path(writable).resolve():return candidate
    except OSError:pass
    return None
