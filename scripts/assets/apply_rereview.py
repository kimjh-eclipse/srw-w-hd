"""Apply the 11/21 re-review (pose_packets/_rereview/MERGED.json + Claude overrides).

Failing unit:
  - bad poses >= 30% of its accepted poses (systematic face/colour error): every HD part this
    unit installed is disabled (original + xBRZ shown) and HOLD_REDRAW is written;
  - fewer bad poses: only parts whose sprite hash appears in the bad poses and in none of the
    good poses are disabled (a part shared with a good pose keeps its HD); HOLD_REDRAW written
    so the bad poses get redrawn.
--hold-only writes HOLD_REDRAW files (safe while the rollout runs; it skips held units).
Report: pose_packets/_rereview/APPLIED.json. Run the full mode under the install lock.

  py -3.11 -X utf8 scripts/assets/apply_rereview.py [--hold-only] [--dry]
"""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
BASE=ROOT/'test_current/parts/pose_packets';RR=BASE/'_rereview'
OK_OVERRIDE={'unit_5':'blue only slightly deeper (Claude check)','unit_314':'hair silver vs grey-beige, minor','unit_358':'glitch frame, minor','unit_154':'helmet eye line minor, same frame as 142 (ok)'}
FAIL_OVERRIDE={'unit_273':{'pose_02':'head turned from profile to front with one big red eye; left arm forward (Claude check)'}}


def main():
    p=argparse.ArgumentParser();p.add_argument('--hold-only',action='store_true');p.add_argument('--dry',action='store_true');a=p.parse_args()
    units=json.loads((RR/'MERGED.json').read_text(encoding='utf-8'))['units']
    for u in OK_OVERRIDE:units[u]=dict(verdict='ok',bad_poses={},note=OK_OVERRIDE[u])
    for u,b in FAIL_OVERRIDE.items():units[u]=dict(verdict='fail',bad_poses=b,note='Claude check')
    fails={u:v for u,v in units.items() if v['verdict']=='fail' and v['bad_poses']}
    lib=None if a.hold_only else json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text(encoding='utf-8'))
    report={};off_total=0
    for u,v in sorted(fails.items(),key=lambda kv:int(kv[0][5:])):
        rs=BASE/u/'robot_set';st=json.loads((rs/'DRAWINGS_STATUS.json').read_text(encoding='utf-8'))
        acc=[k for k,s in st.items() if s.get('state')=='accepted'];bad=[k for k in v['bad_poses'] if k in acc] or list(v['bad_poses'])
        whole=len(bad)>=0.3*max(1,len(acc))
        if not a.dry:(rs/'HOLD_REDRAW').write_text('11/21 re-review: '+json.dumps(v['bad_poses'],ensure_ascii=False),encoding='utf-8')
        row=dict(accepted=len(acc),bad=len(bad),mode='whole' if whole else 'bad-pose parts',bad_poses=v['bad_poses'])
        if lib is not None:
            def hashes(ps):
                out=set()
                for k in ps:
                    c=rs/k/'contract.json'
                    if c.exists():out|={r['hash'] for r in json.loads(c.read_text(encoding='utf-8'))}
                return out
            target=None if whole else hashes(bad)-hashes([k for k in acc if k not in bad])
            n=0
            for b in lib['bindings']:
                if b.get('disabled') or not str(b.get('atlas_id') or '').startswith(u+'_'):continue
                if target is not None and b.get('hash') not in target:continue
                n+=1
                if not a.dry:b['disabled']=True;b['disabled_reason']='11/21 re-review: drawing wrong ('+('whole unit' if whole else 'bad poses')+'); original shown until redraw'
            row['disabled']=n;off_total+=n
        report[u]=row
    if lib is not None and not a.dry:
        (ROOT/'graphics/kazuma_parts_library.json').write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8')
        for s in ('scripts/build/build_native_material_cache.py','scripts/assets/build_material_slot_cache.py','scripts/assets/build_tile_library.py'):
            r=subprocess.run([sys.executable,'-X','utf8',s],cwd=ROOT,capture_output=True);print(s,'ok' if r.returncode==0 else 'FAILED')
    (RR/('APPLIED.json' if not a.dry else 'APPLIED_dry.json')).write_text(json.dumps(report,ensure_ascii=False,indent=1),encoding='utf-8')
    print('failing units',len(report),'whole',sum(r['mode']=='whole' for r in report.values()),'bindings off',off_total)


if __name__=='__main__':main()
