"""Delete per-frame pose folders once a weapon's objects are built.

weapon_*/pose_NNN hold every distinct frame layout (native, 4x, labels) and
are only an input to build_object_packets.py. When weapon_*/objects/INDEX.json
exists the pose folders are no longer needed. robot_set folders and objects
are never touched.

  py -3.11 -X utf8 scripts/assets/prune_pose_captures.py [unit ...]   (default: all units)
"""
import shutil,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def prune_weapon(weapon):
    if not (weapon/'objects'/'INDEX.json').exists():return 0
    n=0
    for p in weapon.glob('pose_*'):
        if p.is_dir() and p.name[5:].isdigit():shutil.rmtree(p,ignore_errors=True);n+=1
    return n


def main():
    base=ROOT/'test_current/parts/pose_packets'
    units=[base/f'unit_{u}' for u in sys.argv[1:]] or sorted(base.glob('unit_*'))
    total=0
    for unit in units:
        for weapon in sorted(unit.glob('weapon_*')):total+=prune_weapon(weapon)
    print('pose folders removed',total)


if __name__=='__main__':main()
