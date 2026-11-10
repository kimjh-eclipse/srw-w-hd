"""Supervise isolated native unit replays; preserve crashes as failures, not coverage.

Each child owns one fixed output folder. A crashed unit is retried weapon by
weapon, allowing the other animations to run without touching player progress.
"""
import sys,json,subprocess,os,argparse,time,threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--workers',type=int,default=6)
    parser.add_argument('--units',default='all');args=parser.parse_args()
    assert 1<=args.workers<=8
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text())
    selected=None if args.units=='all' else set(map(int,args.units.split(',')))
    units=[u for u in catalog['units'] if u['primary_image'] is not None and u['weapon_ids'] and (selected is None or u['unit_id'] in selected)]
    # Exercise newly painted mechanical cut-ins before statistics variants.
    priority={221,223,224,244,295,297,404,413,207,206,218}
    units.sort(key=lambda u:(u['unit_id'] not in priority,u['unit_id']))
    output=ROOT/'test_current/combat/named_attacks';output.mkdir(exist_ok=True)
    env=dict(os.environ,SRWW_STAGE_CACHE_MB='384',PYTHONUTF8='1')
    script=ROOT/'scripts/verify/verify_named_attacks.py'
    def replay(unit):
        uid=unit['unit_id'];folder=output/f'unit_{uid}';folder.mkdir(exist_ok=True)
        base=[sys.executable,'-X','utf8',str(script),'--units',str(uid),'--unit-output','--diagnostic-unlock','--frames','3000','--resume']
        failures=[]
        def run(extra,label):
            with (folder/f'{label}.log').open('w',encoding='utf-8') as log:
                try:return subprocess.run(base+extra,cwd=ROOT,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=420).returncode
                except subprocess.TimeoutExpired:return 'timeout'
        code=run(['--weapons','all'],'replay')
        if code:
            failures.append(dict(scope='unit',exit_code=code))
            for wi,wid in enumerate(unit['weapon_ids']):
                code=run(['--weapon-indices',str(wi)],f'weapon_{wid}')
                if code:failures.append(dict(weapon_id=wid,exit_code=code))
        report=folder/'report.json';rows=json.loads(report.read_text())['rows'] if report.exists() else []
        result=dict(unit_id=uid,name_ja=unit['name_ja'],expected=len(unit['weapon_ids']),attempted=len(rows),
                    verified=sum(r.get('full_replay_verified',False) for r in rows),process_failures=failures,
                    missing_weapon_ids=sorted(set(unit['weapon_ids'])-{r['weapon_id'] for r in rows}))
        (folder/'process_result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
        return result
    results=[];start=time.monotonic()
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for future in as_completed([pool.submit(replay,u) for u in units]):
            results.append(future.result())
            data=dict(scope=__doc__,all_poses_visually_verified=False,expected_units=len(units),finished_units=len(results),
                      expected_weapons=sum(len(u['weapon_ids']) for u in units),
                      verified=sum(r['verified'] for r in results),elapsed_seconds=round(time.monotonic()-start),units=sorted(results,key=lambda r:r['unit_id']))
            target=output/'catalog_progress.json';temporary=target.with_suffix('.tmp.json')
            temporary.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');temporary.replace(target)
            print('units',len(results),'/',len(units),'verified',data['verified'],'last',results[-1]['unit_id'],flush=True)

if __name__=='__main__':main()
