"""Build the attack-start states the unit review cache does not have yet (for cut-in scans).

Every catalog weapon without test_current/gui/unit_review/attack_starts/unit_<U>_weapon_<W>.state
is built with attack_start.build_in_child (one child process per weapon, 4 at a time).
Failures (combination/MAP weapons the builder cannot route) are recorded, not retried.
Safe to stop at any time: finished states stay, the next run skips them.

  py -3.11 -X utf8 scripts/verify/build_missing_attack_starts.py [--workers 4]
"""
import argparse,json,sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))
ROM=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
CACHE=ROOT/'test_current/gui/unit_review/attack_starts';LOG=ROOT/'test_current/parts/cutin_requests/_scan/attack_start_build.json'


def main():
    p=argparse.ArgumentParser();p.add_argument('--workers',type=int,default=4);a=p.parse_args()
    from attack_start import build_in_child
    cat=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text(encoding='utf-8'))
    log=json.loads(LOG.read_text()) if LOG.exists() else {}
    todo=[(u['unit_id'],w) for u in cat['units'] if u.get('primary_image') is not None for w in (u.get('weapon_ids') or [])
          if not (CACHE/f"unit_{u['unit_id']}_weapon_{w}.state").exists() and f"{u['unit_id']}_{w}" not in log]
    print('to build',len(todo),flush=True)
    def one(t):
        u,w=t;r=build_in_child(ROOT,ROM,u,w,CACHE/f'unit_{u}_weapon_{w}.state');return t,r
    done=0
    with ThreadPoolExecutor(a.workers) as ex:
        for (u,w),r in ex.map(one,todo):
            log[f'{u}_{w}']=dict(ok=bool(r.get('ok')),reason=r.get('reason'));done+=1
            if done%20==0:
                LOG.write_text(json.dumps(log,ensure_ascii=False,indent=0),encoding='utf-8');print('built',done,'ok',sum(v['ok'] for v in log.values()),flush=True)
    LOG.write_text(json.dumps(log,ensure_ascii=False,indent=0),encoding='utf-8')
    print('done',done,'ok',sum(v['ok'] for v in log.values()))


if __name__=='__main__':main()
