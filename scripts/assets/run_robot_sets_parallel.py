"""Run run_robot_sets.py in N worker processes over an ordered unit list.

Units are dealt round-robin so the first units (Gundam W series) finish first.
Each worker logs to test_current/parts/pose_packets/worker_<k>.log; units that
already have a PARTITIONS_SHEET.png are skipped, so the run can be restarted.
A unit whose folder exists without a finished sheet is cleared first (partial
capture from a stopped run).

  py -3.11 -X utf8 scripts/assets/run_robot_sets_parallel.py --workers 6 --order test_current/parts/pose_packets/robot_order.txt
"""
import argparse,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def main():
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=6);p.add_argument('--order',type=Path,required=True)
    a=p.parse_args()
    base=ROOT/'test_current/parts/pose_packets'
    order=[int(x) for x in (ROOT/a.order).read_text().split()]
    todo=[]
    for uid in order:
        unit=base/f'unit_{uid}'
        if (unit/'robot_set'/'PARTITIONS_SHEET.png').exists():continue
        if unit.exists():shutil.rmtree(unit)
        todo.append(uid)
    lists=[todo[k::a.workers] for k in range(a.workers)]
    procs=[]
    for k,units in enumerate(lists):
        if not units:continue
        log=(base/f'worker_{k}.log').open('w',encoding='utf-8')
        procs.append(subprocess.Popen([sys.executable,'-X','utf8','scripts/assets/run_robot_sets.py',*map(str,units)],cwd=ROOT,stdout=log,stderr=subprocess.STDOUT))
    print('workers',len(procs),'units',len(todo),flush=True)
    for p_ in procs:p_.wait()
    print('ALL WORKERS DONE',flush=True)


if __name__=='__main__':main()
