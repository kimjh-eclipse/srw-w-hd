"""Disable installed robot parts that were cut from areas mostly hidden in every drawing.

A part (sprite) that the unit's drawings show for less than --min of its pixels
was completed by growing the few drawn pixels (package_robot_set grow_fill), so
the installed HD part is mostly invented: unit 130 frame 240 showed a black and
red hole in the chest (binding 95122, 7.6% drawn in unit 129's set). The
original sprite is shown instead until a drawing shows the part.

Reads each installed unit's split_fit/coverage.json; disables the active binding
of that hash that this unit installed (atlas_id unit_<U>_...).

  py -3.11 -X utf8 scripts/assets/disable_hidden_parts.py [--min 0.5] [--dry]
Run under the install lock (scripts/assets/hidden_parts_queue.sh).
"""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

LIB=ROOT/'graphics/kazuma_parts_library.json'
BASE=ROOT/'test_current/parts/pose_packets'


def main():
    p=argparse.ArgumentParser();p.add_argument('--min',type=float,default=.5);p.add_argument('--dry',action='store_true');p.add_argument('--also',type=int,nargs='*',default=[]);a=p.parse_args()
    low={}
    for f in BASE.glob('unit_*/robot_set/split_fit/coverage.json'):
        rs=f.parent.parent
        if not (rs/'INSTALLED').exists():continue
        u=rs.parent.name[5:]
        for r in json.loads(f.read_text(encoding='utf-8')):
            if r['coverage']<a.min:low.setdefault(r['hash'],set()).add(u)
    lib=json.loads(LIB.read_text(encoding='utf-8'));done=[]
    for i,b in enumerate(lib['bindings'],1):
        if b.get('disabled') or b.get('hash') not in low:continue
        if b.get('hidden_part_reviewed'):continue   # re-enabled after an in-game render showed it correct (reenable_hidden_parts.py)
        aid=str(b.get('atlas_id') or '')
        if not any(aid.startswith(f'unit_{u}_') for u in low[b['hash']]):continue
        if not a.dry:
            b['disabled']=True;b['disabled_reason']=f'part drawn for less than {a.min:.0%} of its pixels in the unit drawings (rest was invented by growing); original shown until a drawing shows it'
        done.append(i)
    for i in a.also:   # bindings found wrong by eye (a part shown wrongly in one pose although well covered in another)
        b=lib['bindings'][i-1]
        if not b.get('disabled') and not a.dry:b['disabled']=True;b['disabled_reason']='wrong shape in the scene where it is shown (eye check); original shown'
        done.append(i)
    if not a.dry:LIB.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8')
    print('hidden-part hashes',len(low),'bindings disabled' if not a.dry else 'would disable',len(done),done[:20])
    (BASE/'HIDDEN_PARTS_DISABLED.json').write_text(json.dumps(dict(min=a.min,dry=a.dry,bindings=done),indent=1),encoding='utf-8')


if __name__=='__main__':main()
