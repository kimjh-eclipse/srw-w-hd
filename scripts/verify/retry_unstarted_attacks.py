"""Retry only native attacks that previously remained at selection/confirmation."""
import argparse,json,os,subprocess,sys
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def main():
    p=argparse.ArgumentParser();p.add_argument('--kind',choices=['confirmation','combination','terrain','level','preview'],default='confirmation');p.add_argument('--workers',type=int,default=3);a=p.parse_args()
    assert 1<=a.workers<=4
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());units={u['unit_id']:u for u in catalog['units']}
    base=ROOT/'test_current/combat/named_attacks';jobs=[]
    for path in sorted(base.glob('unit_*/report.json')):
        rows=[r for r in json.loads(path.read_text(encoding='utf-8'))['rows'] if not r['battle_started'] and ((r.get('blocked_reason')=='weapon_absent_from_native_menu') if a.kind in ('combination','level','preview') else r.get('blocked_reason') is None)]
        if not rows:continue
        uid=rows[0]['unit_id'];indices=[units[uid]['weapon_ids'].index(r['weapon_id']) for r in rows];jobs.append((uid,indices,path.parent))
    def replay(job):
        uid,indices,folder=job;args=[sys.executable,'-X','utf8',str(ROOT/'scripts/verify/verify_named_attacks.py'),'--units',str(uid),'--weapon-indices',','.join(map(str,indices)),'--unit-output','--diagnostic-unlock','--map-aligned-fixture','--frames','6000']
        if a.kind in ('combination','level','preview'):args.append('--combination-fixture')
        if a.kind=='terrain':args.append('--diagnostic-terrain')
        if a.kind in ('level','preview'):args.extend(['--diagnostic-level','--diagnostic-terrain'])
        if a.kind=='preview':args.append('--diagnostic-menu-entry')
        env=dict(os.environ,SRWW_STAGE_CACHE_MB='384')
        with (folder/f'{a.kind}_retry.log').open('w',encoding='utf-8') as log:
            try:code=subprocess.run(args,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600).returncode
            except subprocess.TimeoutExpired:code='timeout'
        return dict(unit_id=uid,weapons=len(indices),exit_code=code)
    results=[]
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for future in as_completed([pool.submit(replay,job) for job in jobs]):
            results.append(future.result());print(results[-1],flush=True)
            (base/f'{a.kind}_retry.json').write_text(json.dumps(dict(scope=__doc__,expected_units=len(jobs),finished_units=len(results),results=results),indent=2))
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'scripts/verify/summarize_named_replays.py')],cwd=ROOT,check=True)

if __name__=='__main__':main()
