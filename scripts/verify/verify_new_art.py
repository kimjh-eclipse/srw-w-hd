"""Check every binding of the production manifest against its native part.

Runs the per-part comparison of audit_all_parts.py (shape, colour, flat,
key colour, empty) on the bindings listed in
docs/PRODUCTION_ART_BATCH_CURRENT.json, reports them per batch, and draws
contact sheets (native | HD) of the flagged parts and of an even sample of
the unflagged ones, because a part that passes the screens can still be a
wrong picture. Reads only; writes test_current/parts/new_art_review/.
"""
import argparse,json,sys
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent))
import audit_all_parts as audit


def work(binding):
    try:return audit.analyse(binding)
    except Exception as error:return dict(binding=binding,skipped='error: '+str(error)[:120])


def sheet(rows,path,title_of,cell=128,per_row=6):
    picture=Image.new('RGB',(per_row*cell*2,((len(rows)+per_row-1)//per_row)*(cell+14)),(40,40,48));draw=ImageDraw.Draw(picture)
    for index,row in enumerate(rows):
        try:_,pixels,reference=audit.analyse(row['binding'],keep=True)
        except Exception:continue
        x=(index%per_row)*cell*2;y=(index//per_row)*(cell+14);scale=min((cell-4)/pixels.shape[1],(cell-4)/pixels.shape[0])
        size=(max(1,round(pixels.shape[1]*scale)),max(1,round(pixels.shape[0]*scale)))
        a=Image.fromarray(reference).resize(size,Image.Resampling.NEAREST);b=Image.fromarray(pixels).resize(size,Image.Resampling.LANCZOS)
        picture.paste(a,(x+2,y+2),a);picture.paste(b,(x+cell+2,y+2),b);draw.text((x+2,y+cell),title_of(row),fill=(230,230,230))
    picture.save(path)


def main():
    parser=argparse.ArgumentParser(description=__doc__.split('\n')[0]);parser.add_argument('--workers',type=int,default=6);parser.add_argument('--sample',type=int,default=240)
    args=parser.parse_args();out=ROOT/'test_current/parts/new_art_review';out.mkdir(parents=True,exist_ok=True)
    for old in out.glob('*'):
        if old.is_file():old.unlink()
    manifest=json.loads((ROOT/'docs/PRODUCTION_ART_BATCH_CURRENT.json').read_text(encoding='utf-8'));owner={}
    for index,batch in enumerate(manifest['batches']):
        for binding in batch.get('current_bindings',batch.get('bindings',[])):owner[int(binding)]=index
    audit.start();renderer=audit._renderer;todo=sorted(b for b in owner if 0<b<=len(renderer.bindings));missing=sorted(b for b in owner if not 0<b<=len(renderer.bindings))
    rows=[];skipped=defaultdict(list)
    with Pool(args.workers,initializer=audit.start) as pool:
        for row in pool.imap_unordered(work,todo,chunksize=32):
            if 'skipped' in row:skipped[row['skipped'].split(':')[0]].append(row['binding'])
            else:row['batch']=owner[row['binding']];rows.append(row)
    flagged=[row for row in rows if row['flags']];counts=defaultdict(int);batches=[]
    for row in flagged:
        for flag in row['flags']:counts[flag]+=1
    for index,batch in enumerate(manifest['batches']):
        mine=[row for row in rows if row['batch']==index];bad=[row for row in mine if row['flags']];flags=defaultdict(int)
        for row in bad:
            for flag in row['flags']:flags[flag]+=1
        listed=batch.get('current_bindings',batch.get('bindings',[]))
        batches.append(dict(batch=index,atlas=batch.get('atlas'),source=batch.get('source'),bindings=len(listed),measured=len(mine),flagged=len(bad),flags=dict(flags),
            unmeasured=[b for b in listed if b not in {row['binding'] for row in mine}],flagged_bindings=[row['binding'] for row in bad]))
    report=dict(manifest_bindings=len(owner),binding_ids_not_in_library=missing,measured=len(rows),skipped={k:len(v) for k,v in skipped.items()},skipped_bindings={k:v[:400] for k,v in skipped.items()},
        flagged=len(flagged),unflagged=len(rows)-len(flagged),rules=audit.RULES,by_flag=dict(sorted(counts.items(),key=lambda item:-item[1])),
        batches_with_flags=sum(1 for b in batches if b['flagged']),batches=sorted(batches,key=lambda b:-b['flagged']),parts=sorted(flagged,key=lambda r:(-len(r['flags']),r['iou'])))
    (out/'report.json').write_text(json.dumps(report,indent=1,ensure_ascii=False),encoding='utf-8');(out/'all_rows.json').write_text(json.dumps(rows),encoding='utf-8')
    label=lambda row:f"#{row['binding']} {str(row['atlas'])[:15]} i{row['iou']:.2f} c{row['colour_bad']:.2f}"
    for flag in audit.RULES:
        group=[row for row in flagged if flag in row['flags']]
        if group:
            order=dict(shape=lambda r:r['iou'],colour=lambda r:-r['colour_bad'],unpainted=lambda r:-r['unpainted'],outside=lambda r:-r['outside'],flat=lambda r:-r['flat'],key_green=lambda r:-r['green_pixels'],key_magenta=lambda r:-r['magenta_pixels'],empty=lambda r:-r['native_texels'])[flag]
            sheet(sorted(group,key=order)[:120],out/f'flag_{flag}.png',label)
    clean=sorted((row for row in rows if not row['flags'] and row['native_texels']>=64),key=lambda r:r['binding'])
    if clean:
        step=max(1,len(clean)//args.sample);picked=clean[::step][:args.sample]
        for page in range(0,len(picked),120):sheet(picked[page:page+120],out/f'unflagged_sample_{page//120:02d}.png',label)
    print(json.dumps({k:v for k,v in report.items() if k not in ('batches','parts','rules','skipped_bindings','binding_ids_not_in_library')},ensure_ascii=False,indent=1))
    print('ids not in library',len(missing))
    for batch in report['batches'][:30]:print(batch['flagged'],'/',batch['bindings'],batch['atlas'],batch['flags'],'unmeasured',len(batch['unmeasured']))


if __name__=='__main__':main()
