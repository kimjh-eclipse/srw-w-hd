"""Replay the native attacks in which newly painted fragments were captured."""
import argparse,json,os,subprocess,sys
from pathlib import Path
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor,as_completed
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--collect-only',action='store_true',help='Collect existing second-pass native reports without replaying');options=parser.parse_args()
    folder=ROOT/'graphics/named_attack_frames';accepted={r['resource'] for r in json.loads((folder/'registration.json').read_text())['accepted']}
    old=json.loads((ROOT/'test_current/parts/observed_attack_gaps/report.json').read_text());chosen={}
    for row in old['unmatched_rectangles']:
        for candidate in row['candidates']:
            resource=candidate['resource']
            if resource in accepted and resource not in chosen:chosen[resource]=(row['unit_id'],row['weapon_id'])
    # Distinct Dominion palette/index variant of the Archangel gun bank.
    if 8265 in accepted:chosen[8265]=(83,355)
    catalog=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());units={u['unit_id']:u for u in catalog['units']};jobs=defaultdict(set)
    for uid,wid in chosen.values():jobs[uid].add(wid)
    def run(uid,wids):
        indices=[units[uid]['weapon_ids'].index(wid) for wid in sorted(wids)]
        args=[sys.executable,'-X','utf8',str(ROOT/'scripts/verify/verify_named_attacks.py'),'--units',str(uid),'--weapon-indices',','.join(map(str,indices)),'--unit-output','--diagnostic-unlock','--map-aligned-fixture','--combination-fixture','--warm-replay','--frames','6000']
        out=ROOT/f'test_current/combat/named_attacks/unit_{uid}'
        code=0
        if not options.collect_only:
            with (out/'new_attack_frames.log').open('w',encoding='utf-8') as log:
                code=subprocess.run(args,cwd=ROOT,env=dict(os.environ,SRWW_STAGE_CACHE_MB='384'),stdout=log,stderr=subprocess.STDOUT,timeout=600).returncode
        rows=[r for r in json.loads((out/'report.json').read_text(encoding='utf-8'))['rows'] if r['weapon_id'] in wids]
        assert len(rows)==len(wids),(uid,'Missing native report rows')
        return dict(unit_id=uid,exit_code=code,rows=[dict(weapon_id=r['weapon_id'],weapon_name=r['weapon_name'],full_replay_verified=r['full_replay_verified'],routed_correctly=r['weapon_routed_correctly'],observed_binding_count=len(r['observed_bindings']),observed_new_source_resources=sorted(accepted.intersection(r.get('observed_source_resources',[]))),cache_warm_replay_pass=r.get('cache_warm_replay_pass'),cutin_ids=r['cutin_ids'],errors=r['errors']) for r in rows])
    results=[]
    with ThreadPoolExecutor(max_workers=3) as executor:
        for future in as_completed([executor.submit(run,uid,wids) for uid,wids in jobs.items()]):
            results.append(future.result());print(results[-1],flush=True)
    observed={v for r in results for w in r['rows'] for v in w['observed_new_source_resources']}
    result=dict(scope=__doc__,resource_native_cases={str(k):list(v) for k,v in chosen.items()},results=results,observed_new_resources=sorted(observed),not_observed_new_resources=sorted(accepted-observed),all_sampled_attacks_completed=all(r['exit_code']==0 and all(w['full_replay_verified'] and w['routed_correctly'] and w['cache_warm_replay_pass']==2 and not w['errors'] for w in r['rows']) for r in results),all_gameplay_poses_visually_verified=False)
    (folder/'gameplay.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    assert result['all_sampled_attacks_completed'],result

if __name__=='__main__':main()
