"""Undo the robot-set installs of given units (user decision 11/16: style-rejected 14, 15, 27, 28, 29).

For each install record of the unit (docs/ART_INSTALL_DONE.json, source pose_packets/unit_<U>/):
  - new parts: the bindings are disabled (kept in the library, not drawn);
  - replaced parts: each binding's library entry is restored from git at the
    commit before the install (--before <commit>), unless a later install of
    another source replaced the same binding again (then it is left alone).
The records get 'reverted' and the unit's INSTALLED marker becomes HOLD_REDRAW.
Caches are rebuilt by running install_pending_art's rebuild at the end.

  py -3.11 -X utf8 scripts/assets/revert_unit_installs.py --unit 14 --before 7611aa73 --unit 15 --before 7611aa73 ...
"""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

LIB=ROOT/'graphics/kazuma_parts_library.json';DONE=ROOT/'docs/ART_INSTALL_DONE.json'


def main():
    p=argparse.ArgumentParser();p.add_argument('--unit',type=int,action='append',required=True);p.add_argument('--before',action='append',required=True)
    a=p.parse_args();assert len(a.unit)==len(a.before)
    lib=json.loads(LIB.read_text(encoding='utf-8'));done=json.loads(DONE.read_text(encoding='utf-8'));recs=done['installed']
    old_libs={}
    stamp=lambda r:str(r.get('installed',''))
    for u,before in zip(a.unit,a.before):
        if before not in old_libs:
            old_libs[before]=json.loads(subprocess.run(['git','show',f'{before}:graphics/kazuma_parts_library.json'],cwd=ROOT,capture_output=True,text=True,encoding='utf-8').stdout)['bindings']
        old=old_libs[before];key=f'unit_{u}/'
        mine=[r for r in recs if key in str(r.get('source','')).replace('\\','/') and not r.get('reverted')]
        for r in mine:
            ids=r['bindings'] if isinstance(r['bindings'],list) else json.loads(r['bindings'])
            if r.get('new_parts'):
                for b in ids:lib['bindings'][b-1]['disabled']=True;lib['bindings'][b-1]['disabled_reason']=f'unit {u} redraw reverted (user 11/16 style rejection)'
                print(u,'new parts disabled',len(ids))
            else:
                restored=kept=0
                for b in ids:
                    later=[o for o in recs if o is not r and stamp(o)>stamp(r) and b in (o['bindings'] if isinstance(o['bindings'],list) else json.loads(o['bindings'])) and not o.get('reverted') and key not in str(o.get('source','')).replace('\\','/')]
                    if later:kept+=1;continue
                    lib['bindings'][b-1]=old[b-1] if b<=len(old) else dict(lib['bindings'][b-1],disabled=True);restored+=1
                print(u,'replaced parts restored',restored,'kept (replaced again later)',kept)
            r['reverted']='user 11/16: style rejected, install undone'
        rs=ROOT/f'test_current/parts/pose_packets/unit_{u}/robot_set'
        (rs/'INSTALLED').unlink(missing_ok=True);(rs/'HOLD_REDRAW').write_text('user 11/16: style-rejected drawing; install reverted, waiting for the redraw\n',encoding='utf-8')
    LIB.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8');DONE.write_text(json.dumps(done,ensure_ascii=False,indent=1),encoding='utf-8')
    for s in ('scripts/build/build_native_material_cache.py','scripts/assets/build_material_slot_cache.py','scripts/assets/build_tile_library.py'):
        r=subprocess.run([sys.executable,'-X','utf8',s],cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace');print(s,'ok' if r.returncode==0 else 'FAILED '+(r.stderr.strip().splitlines() or [''])[-1])


if __name__=='__main__':main()
