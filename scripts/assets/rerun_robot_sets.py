"""Re-select robot sets for units already captured (no new capture).

Skips units whose robot_set holds drawings. Per unit: build_unit_robot_set,
round-trip split check, partition sheet, pose sheet.

  py -3.11 -X utf8 scripts/assets/rerun_robot_sets.py [unit ...]   (default: every captured unit)
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets.run_robot_sets import step,pose_sheet


def main():
    base=ROOT/'test_current/parts/pose_packets'
    units=[int(x) for x in sys.argv[1:]] or sorted(int(p.parent.parent.name[5:]) for p in base.glob('unit_*/robot_set/PARTITIONS_SHEET.png'))
    for uid in units:
        rs=base/f'unit_{uid}'/'robot_set'
        if any(rs.glob('pose_*/candidate*.png')):print(uid,'has drawings, kept',flush=True);continue
        code,last,err=step(['scripts/assets/build_unit_robot_set.py','--unit',str(uid)])
        if code:print(uid,'set failed',err,flush=True);continue
        step(['scripts/assets/split_object_drawings.py',str(rs),'--selftest']);step(['scripts/verify/partition_sheet.py',str(rs)])
        try:pose_sheet(rs)
        except Exception as e:print(uid,'sheet failed',e,flush=True);continue
        print(uid,'reselected',last[:160],flush=True)
    print('RERUN DONE',flush=True)


if __name__=='__main__':main()
