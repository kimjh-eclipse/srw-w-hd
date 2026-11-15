"""Colour states of a unit: palettes other than the main one that its robot sprites are shown in.

A colour state = one whole-robot palette (a fade step, a flash, a tint). For
each state: the robot objects shown in it, how many distinct shapes, and how
many frames it is on screen. Writes <set>/VARIANT_STATES.json.

  py -3.11 -X utf8 scripts/assets/variant_states.py <unit> [<unit> ...]
"""
import json,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

BASE=ROOT/'test_current/parts/pose_packets'


def states(u):
    rs=BASE/f'unit_{u}/robot_set';shapes=json.loads((rs/'SHAPES.json').read_text(encoding='utf-8'))
    main=set(shapes['main_palette'].values());robot_hashes={h for v in shapes['variants'].values() for h in v}
    st=defaultdict(lambda:dict(objects=[],shapes=set(),frames=0))
    for folder in sorted((BASE/f'unit_{u}').glob('weapon_*/objects/obj_*')):
        rows=json.loads((folder/'contract.json').read_text(encoding='utf-8'))
        robot=[r for r in rows if r['hash'] in robot_hashes]
        if not robot or all(r['hash'] in main for r in robot):continue
        # The state is the set of robot palettes in the object (usually one bank).
        key=tuple(sorted({tuple(r['palette_15bit']) for r in robot if r['hash'] not in main}))
        frames=len(json.loads((folder/'frames.json').read_text())['frames'])
        s=st[key];s['objects'].append(str(folder.relative_to(BASE)).replace('\\','/'));s['shapes']|={r['index_hash'] for r in robot};s['frames']+=frames
    out=[dict(state=n,palettes=[list(p) for p in k],objects=len(v['objects']),shapes=len(v['shapes']),frames=v['frames'],object_list=v['objects']) for n,(k,v) in enumerate(sorted(st.items(),key=lambda kv:-kv[1]['frames']))]
    (rs/'VARIANT_STATES.json').write_text(json.dumps(out,ensure_ascii=False,indent=1),encoding='utf-8')
    return out


def main():
    total_states=total_objects=0
    for u in map(int,sys.argv[1:]):
        try:out=states(u)
        except FileNotFoundError:print(u,'no set');continue
        total_states+=len(out);total_objects+=sum(s['objects'] for s in out)
        print(u,'states',len(out),'objects',sum(s['objects'] for s in out),'frames',sum(s['frames'] for s in out),'top',[(s['shapes'],s['frames']) for s in out[:6]])
    print('TOTAL states',total_states,'objects',total_objects)


if __name__=='__main__':main()
