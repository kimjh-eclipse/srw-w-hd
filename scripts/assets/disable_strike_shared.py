"""Strike family (units 11-22, Rouge 39-45): show the original sprite for every part shared by 2+ units.

The family shares its body sprites (same hash) across all variants, and one hash has one HD
texture, so each variant's install overwrote the others' cut of the same part: pieces from
different drawings did not line up (stair-step edges, chest/arm seams; user review 2026-11-19).
Other SEED units were checked in game and are fine, so only this family is changed.

  py -3.11 -X utf8 scripts/assets/disable_strike_shared.py [--dry]
Run under the install lock. Reads the hash list computed from the pose contracts.
"""
import argparse,collections,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

FAMILY={11,12,13,14,15,16,17,18,19,20,21,22,39,40,41,42,43,44,45}
LIB=ROOT/'graphics/kazuma_parts_library.json'
BASE=ROOT/'test_current/parts/pose_packets'


def main():
    p=argparse.ArgumentParser();p.add_argument('--dry',action='store_true');a=p.parse_args()
    units_of=collections.defaultdict(set)
    for c in BASE.glob('unit_*/robot_set/pose_*/contract.json'):
        u=int(c.parts[-4][5:])
        try:rows=json.loads(c.read_text(encoding='utf-8'))
        except Exception:continue
        if isinstance(rows,list):
            for r in rows:units_of[r['hash']].add(u)
    shared={h for h,us in units_of.items() if len(us)>=2 and us&FAMILY}
    outside={h for h in shared if units_of[h]-FAMILY}
    shared-=outside   # never touch a part another (non-Strike) unit also uses
    lib=json.loads(LIB.read_text(encoding='utf-8'));done=[]
    for i,b in enumerate(lib['bindings'],1):
        if b.get('disabled') or b.get('hash') not in shared:continue
        if not a.dry:
            b['disabled']=True;b['disabled_reason']='Strike family part shared by several units: their drawings overwrite one texture and do not line up; original shown (2026-11-19)'
        done.append(i)
    if not a.dry:LIB.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8')
    print('shared family hashes',len(shared),'skipped (used outside family)',len(outside),'bindings','would disable' if a.dry else 'disabled',len(done))
    (BASE/'STRIKE_SHARED_DISABLED.json').write_text(json.dumps(dict(dry=a.dry,hashes=sorted(shared),bindings=done),indent=1),encoding='utf-8')


if __name__=='__main__':main()
