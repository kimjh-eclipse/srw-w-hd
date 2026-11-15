"""Install reviewed robot sets: split fitted drawings, package, queue, check, apply.

Per unit (test_current/parts/pose_packets/unit_<U>/robot_set):
  only poses 'accepted' in DRAWINGS_STATUS.json are used;
  split_object_drawings (candidate_fit.png) -> package_robot_set -> queue entries
  -> install_pending_art precheck -> --apply.
Stops before a unit when C: has less than --min-free GB.
Caches are rebuilt once, after the last unit (--no-caches on the others).

  py -3.11 -X utf8 scripts/assets/install_unit_sets.py 7 8 15 [--min-free 3]
"""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

PY=[sys.executable,'-X','utf8']


def run(*a,check=True):
    r=subprocess.run(PY+[str(x) for x in a],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace')
    if check and r.returncode:raise RuntimeError(f"{a[0]} failed: {(r.stderr or r.stdout).strip().splitlines()[-1:]}")
    return r.stdout


def main():
    p=argparse.ArgumentParser();p.add_argument('units',nargs='+',type=int);p.add_argument('--min-free',type=float,default=3)
    a=p.parse_args();results={}
    for n,u in enumerate(a.units):
        free=shutil.disk_usage(ROOT).free/2**30
        if free<a.min_free:print('STOP low disk',round(free,1),'GB before unit',u,flush=True);break
        rs=ROOT/f'test_current/parts/pose_packets/unit_{u}/robot_set'
        if (rs/'HOLD_REDRAW').exists():print(u,'held for redraw, not installed',flush=True);continue
        status=json.loads((rs/'DRAWINGS_STATUS.json').read_text(encoding='utf-8'))
        accepted=[k for k,v in status.items() if v['state']=='accepted']
        if not accepted:print(u,'nothing accepted',flush=True);continue
        only=rs/'accepted_poses.json';only.write_text(json.dumps(accepted),encoding='utf-8')
        split=rs/'split_fit'
        if split.exists():shutil.rmtree(split)
        try:
            run('scripts/assets/split_object_drawings.py',rs,'--drawing','candidate_fit.png','--out',split,'--only',only)
            q=ROOT/'docs/PENDING_ART_INSTALL_QUEUE.json';queue=json.loads(q.read_text(encoding='utf-8'));sources=[]
            inst=rs/'install'
            if inst.exists():shutil.rmtree(inst)
            run('scripts/assets/package_robot_set.py',rs)
            for f in sorted(inst.glob('*/queue_entry.json')):
                e=json.loads(f.read_text(encoding='utf-8'));sources.append(e['source'])
                queue['ready_candidates']=[c for c in queue['ready_candidates'] if c.get('source')!=e['source']]+[e]
            q.write_text(json.dumps(queue,ensure_ascii=False,indent=1),encoding='utf-8')
            if not sources:
                results[u]=dict(poses=len(accepted),lines=['all parts already redrawn by other units']);print(u,'poses',len(accepted),'all parts already redrawn by other units',flush=True);continue
            # Originals (1..5263) of this unit are replaced under the user's whole-robot redraw order.
            originals=[]
            for f in inst.glob('*_replace/contract.json'):originals+=[r['replace_binding'] for r in json.loads(f.read_text(encoding='utf-8')) if r['replace_binding']<=5263]
            allow=['--allow-original',*originals] if originals else []
            run('scripts/assets/install_pending_art.py','--only',*sources)
            flags=([] if n==len(a.units)-1 else ['--no-caches'])+allow
            out=run('scripts/assets/install_pending_art.py','--apply','--only',*sources,*flags)
            lines=[l for l in out.splitlines() if l.startswith(('new parts','installed','NOT INSTALLED','FAILED'))]
            results[u]=dict(poses=len(accepted),lines=lines);print(u,'poses',len(accepted),' | '.join(l[:160] for l in lines),flush=True)
        except RuntimeError as e:
            results[u]=dict(error=str(e));print(u,'ERROR',e,flush=True)
    (ROOT/'test_current/parts/pose_packets/INSTALL_LOG.json').write_text(json.dumps(results,ensure_ascii=False,indent=1),encoding='utf-8')


if __name__=='__main__':main()
