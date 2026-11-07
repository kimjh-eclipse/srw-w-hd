"""Freeze a compact whole-texture plan for every reviewed mechanical candidate.

This does not certify PAT association or claim complete in-game coverage.
Never repack a plan once generated art exists.
"""
from pathlib import Path
from functools import lru_cache
import sys,json,hashlib
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/animation_parts';TARGET=OUT/'full_attack_sheets.json'
if TARGET.exists():
    p=json.loads(TARGET.read_text());print(json.dumps(dict(frozen_plan=True,sheets=len(p['sheets']))));raise SystemExit
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
@lru_cache(maxsize=128)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
audit=json.loads((ROOT/'test_current/rom_catalog/animation_audit.json').read_text());palettes={i:p['palette'] for p in audit['patterns'] for i in p['image_group']}
review=json.loads((OUT/'scope_review.json').read_text());ids=[p['image'] for p in review['items'] if p['classification']=='mechanical_or_attached_effect']
old=json.loads((ROOT/'graphics/all_units/batches.json').read_text());existing={s['resource']:dict(atlas_id='all_'+b['name'],x=0,y=s['batch_y']) for b in old['batches'] if b.get('required') for s in b['segments'] if s['resource']!=7406}
late=json.loads((OUT/'late_attack_sheets.json').read_text())
for b in late['sheets']:
    if (OUT/b['image']).exists():
        for s in b['segments']:existing[s['resource']]=dict(atlas_id=b['name'],x=s['x'],y=s['y'],palette_rgb=s['palette_rgb'])
items=[];duplicates={};seen={};unresolved=[]
for i in ids:
    if i in existing:continue
    a=g.pixels(resource(i));digest=hashlib.sha256(a.tobytes()+str(a.shape).encode()).hexdigest()
    if digest in seen:duplicates[i]=seen[digest];continue
    seen[digest]=i;colors=np.asarray(g.palette(resource(palettes[i])),dtype='uint8');used=np.unique(a[a!=0]);assert a.max()<16
    banks=[colors[b:b+16] for b in range(0,len(colors),16) if len(colors[b:b+16])>int(a.max())]
    if not banks:
        unresolved.append(dict(image=i,palette=palettes[i],palette_colors=len(colors),largest_index=int(a.max()),reason='Partial/shared palette needs runtime association'))
        continue
    pal=max(banks,key=lambda p:len(np.unique(p[used,:3],axis=0)))
    if len(pal)<16:pal=np.concatenate([pal,np.repeat(pal[-1:],16-len(pal),axis=0)])
    rgba=pal[a].copy();rgba[:,:,3]=np.where(a,255,0);rgba[a==0,:3]=0
    items.append((i,Image.fromarray(rgba),pal[:,:3].tolist()))
if unresolved:
    (OUT/'full_attack_blockers.json').write_text(json.dumps(dict(unresolved_palettes=unresolved,ready_unique_sources=len(items),duplicates=len(duplicates),complete=False),indent=2))
    print(json.dumps(dict(unresolved_palettes=len(unresolved),ready_unique_sources=len(items),packing_started=True)))
sheets=[];segments=[];canvas=Image.new('RGBA',(544,544));x=y=row=6
def flush():
    global canvas,segments,x,y,row
    if not segments:return
    name=f'full_attack_{len(sheets):03}';canvas.save(OUT/f'{name}_native.png');canvas.resize((2176,2176),Image.Resampling.NEAREST).save(OUT/f'{name}_reference.png')
    sheets.append(dict(name=name,native_size=[544,544],reference=f'{name}_reference.png',image=f'{name}_hd.png',segments=segments));canvas=Image.new('RGBA',(544,544));segments=[];x=y=row=6
for i,im,pal in sorted(items,key=lambda p:(-p[1].height,-p[1].width,p[0])):
    w,h=im.size
    if x+w+6>544:x=6;y+=row+6;row=6
    if y+h+6>544:flush()
    canvas.paste(im,(x,y));segments.append(dict(resource=i,x=x,y=y,w=w,h=h,palette_rgb=pal));x+=w+6;row=max(row,h)
flush();plan=dict(reviewed_mechanical_candidate_images=len(ids),existing_source_atlases=existing,unique_new_images=len(items),duplicates=duplicates,sheets=sheets,source_associations_fully_verified=False,complete=False)
TARGET.write_text(json.dumps(plan,indent=2));print(json.dumps(dict(new_images=len(items),duplicate_images=len(duplicates),sheets=len(sheets),existing=len(existing))))
