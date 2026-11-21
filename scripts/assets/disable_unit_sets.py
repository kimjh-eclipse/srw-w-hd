"""Turn off the installed HD robot parts of whole units (wrong drawings found after install).

Disables every active binding whose atlas was installed from those units' robot sets
(atlas_id unit_<U>_...), so the original sprites (with the xBRZ filter) show until the redraw
is installed. Run under the install lock; caches are rebuilt.

  py -3.11 -X utf8 scripts/assets/disable_unit_sets.py --units 74,75,76,93 --reason "..." [--dry]
"""
import argparse,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT


def main():
    p=argparse.ArgumentParser();p.add_argument('--units',required=True);p.add_argument('--reason',required=True);p.add_argument('--dry',action='store_true');a=p.parse_args()
    pre=tuple(f'unit_{u}_' for u in a.units.split(','))
    path=ROOT/'graphics/kazuma_parts_library.json';lib=json.loads(path.read_text(encoding='utf-8'));off=[]
    for i,b in enumerate(lib['bindings'],1):
        if not b.get('disabled') and str(b.get('atlas_id') or '').startswith(pre):
            off.append(i)
            if not a.dry:b['disabled']=True;b['disabled_reason']=a.reason
    print('would disable' if a.dry else 'disabled',len(off))
    if a.dry or not off:return
    path.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8')
    for s in ('scripts/build/build_native_material_cache.py','scripts/assets/build_material_slot_cache.py','scripts/assets/build_tile_library.py'):
        r=subprocess.run([sys.executable,'-X','utf8',s],cwd=ROOT,capture_output=True);print(s,'ok' if r.returncode==0 else 'FAILED')


if __name__=='__main__':main()
