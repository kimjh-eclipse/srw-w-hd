"""Sort the flagged bindings of verify_new_art.py by what is wrong with them.

Adds two measurements per flagged part (how far the painted mass sits from
the native mass, and how much area it covers compared with the native
part) and names the defect: empty, misplaced, lost (pieces missing or lines
thinned away), bloated, colour, shape. Writes classified.json and one
contact sheet per batch kind. Reads only.
"""
import argparse,json,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent))
import audit_all_parts as audit
from verify_new_art import sheet


def measure(binding):
    row,pixels,reference=audit.analyse(binding,keep=True);native=reference[:,:,3]>0;h,w=native.shape
    cover=(pixels[:,:,3]>=128).reshape(h,4,w,4).swapaxes(1,2).reshape(h,w,16).mean(2);painted=cover>=.5
    ratio=float(painted.sum()/max(1,native.sum()));shift=None
    if native.any() and painted.any():
        ny,nx=np.nonzero(native);py,px=np.nonzero(painted);shift=float(np.hypot(ny.mean()-py.mean(),nx.mean()-px.mean()))
    return ratio,shift,float(np.hypot(*np.ptp(np.nonzero(native),axis=1))) if native.any() else 0.


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('--out',default='test_current/parts/new_art_review')
    parser.add_argument('--no-quarantine-write',action='store_true',help='Leave the shared runtime quarantine list unchanged')
    args=parser.parse_args();out=(ROOT/args.out).resolve()
    if not out.is_relative_to((ROOT/'test_current/parts').resolve()) or out==(ROOT/'test_current/parts').resolve():
        parser.error('--out must be a subdirectory of test_current/parts')
    report=json.loads((out/'report.json').read_text(encoding='utf-8'));audit.start()
    batches={b['batch']:b for b in report['batches']};rows=[]
    for row in report['parts']:
        ratio,shift,extent=measure(row['binding']);flags=row['flags']
        if 'empty' in flags or ratio<.05:kind='empty'
        elif shift is not None and shift>max(2.,.25*max(extent,1)) :kind='misplaced'
        elif ratio<.6 or 'unpainted' in flags:kind='lost'
        elif ratio>1.6 or 'outside' in flags:kind='bloated'
        elif flags==['colour'] or ('colour' in flags and row['iou']>=.6):kind='colour'
        else:kind='shape'
        atlas=str(row['atlas']);effect=atlas.startswith(('observed_effect','reviewed_effect','observed_energy')) or 'effect' in atlas or 'fx' in atlas.lower()
        rows.append(dict(row,area_ratio=round(ratio,3),centroid_shift=None if shift is None else round(shift,2),kind=kind,effect=effect,source=batches[row['batch']]['source']))
    counts=defaultdict(lambda:defaultdict(int));per_batch=defaultdict(lambda:defaultdict(int))
    for row in rows:counts['effect' if row['effect'] else 'machine'][row['kind']]+=1;per_batch[row['atlas']][row['kind']]+=1
    summary=dict(flagged=len(rows),by_group={k:dict(v) for k,v in counts.items()},
        batches=sorted(({'atlas':k,'total_flagged':sum(v.values()),'bindings_in_batch':next((b['bindings'] for b in report['batches'] if b['atlas']==k),None),**v} for k,v in per_batch.items()),key=lambda e:-e['total_flagged']),parts=rows)
    (out/'classified.json').write_text(json.dumps(summary,indent=1,ensure_ascii=False),encoding='utf-8')
    # Effect pictures that failed stay native until they are re-drawn: the list
    # is tied to the failed picture's texture key, so a re-bake releases it.
    renderer=audit._renderer;held={}
    for row in rows:
        if not row['effect']:continue
        spec=renderer.bindings[row['binding']-1];held[str(row['binding'])]=renderer.texture_key(row['binding'],spec['w'],spec['h'])
    if not args.no_quarantine_write:
        (ROOT/'graphics/quarantined_parts.json').write_text(json.dumps(dict(note='Effect parts whose HD picture failed verify_new_art.py; native stays until the picture is re-baked.',
            reasons={str(row['binding']):row['kind'] for row in rows if row['effect']},parts=held),indent=1),encoding='utf-8')
    print('quarantine candidates' if args.no_quarantine_write else 'quarantined',len(held))
    label=lambda row:f"#{row['binding']} {str(row['atlas'])[:14]} {row['kind'][:5]} a{row['area_ratio']:.1f}"
    machines=sorted((row for row in rows if not row['effect']),key=lambda r:(r['atlas'],r['binding']))
    for page in range(0,len(machines),120):sheet(machines[page:page+120],out/f'machines_flagged_{page//120:02d}.png',label)
    for kind in ('misplaced','lost','bloated','colour','shape'):
        group=[row for row in rows if row['effect'] and row['kind']==kind]
        if group:sheet(group[::max(1,len(group)//60)][:60],out/f'effects_{kind}.png',label)
    print(json.dumps({k:v for k,v in summary.items() if k not in ('parts','batches')},ensure_ascii=False))
    print('machine batches:',[(b['atlas'],b['total_flagged'],b['bindings_in_batch']) for b in summary['batches'] if not b['atlas'].startswith('observed_effect')][:40])


if __name__=='__main__':main()
