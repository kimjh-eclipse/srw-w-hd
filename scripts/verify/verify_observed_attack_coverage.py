"""Recheck historical missing rectangles against the current production tile DB.

Old diagnostics are not current missing-asset counts. This runs the actual
assembler on retained native pixels, including locked-animation previews.
"""
import json,sys,time
from pathlib import Path
from collections import Counter
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from tile_compositor import TileCompositor

def main():
    folder=ROOT/'test_current/parts/observed_attack_gaps';report=json.loads((folder/'report.json').read_text())
    compositor=TileCompositor();rows=[];opened=None;active_path=None;started=time.monotonic()
    try:
        for n,record in enumerate(report['unmatched_rectangles']):
            uid,wid=record['unit_id'],record['weapon_id'];base=ROOT/f'test_current/combat/named_attacks/unit_{uid}'
            paths=[ROOT/record['capture']] if record.get('capture') else [base/f'unit_{uid}_weapon_{wid}_unknown.npz',base/f'diagnostic_preview/unit_{uid}_weapon_{wid}_unknown.npz']
            found=False;art=None;stats={}
            for path in paths:
                if not path.exists():continue
                if path!=active_path:
                    if opened is not None:opened.close()
                    opened=np.load(path);active_path=path
                for raw,pixels,palette in zip(opened['rows'],opened['pixels'],opened['palettes']):
                    if (int(raw[0]),int(raw[7]))!=(record['index_hash'],record['material_hash']):continue
                    w,h=map(int,raw[1:3]);art,stats=compositor.assemble(pixels[:w*h].reshape(h,w),palette);found=True;break
                if found:break
            rows.append(dict(unit_id=uid,weapon_id=wid,index_hash=record['index_hash'],material_hash=record['material_hash'],
                capture_found=found,assembled=art is not None,stats=stats,candidates=record['candidates']))
            if n%100==0:print(n,'checked, now assembled',sum(r['assembled'] for r in rows),flush=True)
        counts=Counter(r['candidates'][0]['resource'] for r in rows if r['capture_found'] and not r['assembled'] and r['candidates'])
        result=dict(scope=__doc__,rectangles=len(rows),capture_found=sum(r['capture_found'] for r in rows),
            assembled=sum(r['assembled'] for r in rows),remaining_sources=counts.most_common(),
            seconds=round(time.monotonic()-started,2),all_gameplay_poses_verified=False,rows=rows)
        (folder/'current_assembly.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k!='rows'}))
    finally:
        if opened is not None:opened.close()
        compositor.db.close()

if __name__=='__main__':main()
