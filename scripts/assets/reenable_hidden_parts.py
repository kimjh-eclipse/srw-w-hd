"""Re-enable hidden-part disables that an in-game render showed correct.

disable_hidden_parts.py disables a part drawn for <50% of its pixels in the unit
drawings. While disabled, its native pixels count in the core's unit fallback
vote (srww_parts_impl.h, 10% per palette slot), so one such part can turn the
whole robot back to original dots. The parts below were rendered re-enabled on
11/18 (unit 142 weapon 592 frame 540, unit 59 weapon 273 frame 226): the robot
became fully HD with no hole or invented area visible. They are marked
hidden_part_reviewed so disable_hidden_parts.py leaves them alone.

  py -3.11 -X utf8 scripts/assets/reenable_hidden_parts.py <hash> [<hash> ...]
Run under the install lock (scripts/assets/reenable_hidden_parts.sh). Undo: set
"disabled": true on the listed bindings again.
"""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT

LIB=ROOT/'graphics/kazuma_parts_library.json'


def main():
    hashes={int(x) for x in sys.argv[1:]}
    lib=json.loads(LIB.read_text(encoding='utf-8'));done=[]
    for i,b in enumerate(lib['bindings'],1):
        if b.get('hash') not in hashes or not b.get('disabled'):continue
        if not str(b.get('disabled_reason','')).startswith('part drawn for less'):continue
        b.pop('disabled',None);b['hidden_part_reviewed']='2026-11-18 in-game render check (was: '+b.pop('disabled_reason','')[:60]+')'
        done.append(i)
    if done:LIB.write_text(json.dumps(lib,ensure_ascii=False,indent=2),encoding='utf-8')
    print('re-enabled',done)


if __name__=='__main__':main()
