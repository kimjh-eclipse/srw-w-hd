"""Capture a true native baseline in an isolated core process."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from hd_core import Core
from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state', type=Path, required=True)
    parser.add_argument('--frames', type=int, nargs='+', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    offsets = set(args.frames)
    if min(offsets) < 0:
        parser.error('Frame offsets must be nonnegative.')
    output = args.output.resolve()
    output.relative_to((ROOT / 'test_current').resolve())
    output.mkdir(parents=True, exist_ok=True)
    core = Core(ROOT / 'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',
                demo=True, user_dir=output / 'isolated_saves')
    try:
        core.load(args.state.resolve())
        core.set_hd(False)
        for frame in range(max(offsets) + 1):
            core.run()
            core.audio.clear()
            if frame in offsets:
                Image.fromarray(core.native[:192].copy()).save(output / f'native_{frame}.png')
        (output / 'reference.json').write_text(json.dumps(dict(
            state=str(args.state.resolve()), core=core.core_path, hd_enabled=False,
            frame_convention='zero-based offset after run(), identical to verify_runtime_path',
            frames=sorted(offsets)), indent=2), encoding='utf-8')
    finally:
        core.close()


if __name__ == '__main__':
    main()
