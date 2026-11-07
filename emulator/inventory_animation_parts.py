"""Compare all decoded animation rectangles with the installed HD identities."""
from pathlib import Path
import sys,json,hashlib,zlib,collections,time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'test_current/rom_catalog'
rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
audit=json.loads((OUT/'animation_audit.json').read_text());meta=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
known={b['index_hash']:i for i,b in enumerate(meta['bindings'],1) if b.get('index_hash') and b.get('indexed_safe',True)}
# The approved hero atlas also contains size variants which were indexed only
# by RGB before dynamic palette matching was added.
raw=np.frombuffer((ROOT/'test_current/robot/vram_65340.bin').read_bytes()[:16384],dtype='uint8')
hero=np.stack([raw&15,raw>>4],-1).reshape(16,32,8,8).transpose(0,2,1,3).reshape(128,256)
for i,b in enumerate(meta['bindings'][:4459],1):
    x,y,w,h=[b[k] for k in ('x','y','w','h')];a=hero[y:y+h,x:x+w]
    data=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2')
    known.setdefault(zlib.crc32(data.tobytes())^(w<<16)^h,i)
images={};patterns={};banks={}
for p in audit['patterns']:
    group=p['image_group']
    for image in group:
        if not (1260<=image<3500 or 4395<image<=22696):continue
        images.setdefault(image,set()).update((q['tile'],q['w'],q['h'],q['palette_bank']) for q in p['parts'])
        patterns.setdefault(image,set()).add(p['pattern']);banks[image]=p['palette']
novel={};covered=0;invalid=[];empty=0;total=0;image_stats=[];started=time.time()
for number,(image,rects) in enumerate(sorted(images.items())):
    indexed=g.pixels(resource(image));height,width=indexed.shape;valid=0;new=0;seen=0
    for tile,w,h,bank in sorted(rects):
        x=tile%32*8;y=tile//32*8
        if x+w>width or y+h>height:
            invalid.append(dict(image=image,tile=tile,w=w,h=h,bank=bank));continue
        a=indexed[y:y+h,x:x+w];opaque=int(np.count_nonzero(a))
        if not opaque:empty+=1;continue
        total+=1;valid+=1;data=np.where(a,a.astype('uint16')|0x8000,0).astype('<u2');key=zlib.crc32(data.tobytes())^(w<<16)^h
        if key in known:covered+=1;seen+=1;continue
        if key not in novel:
            novel[key]=dict(index_hash=key,image=image,palette=banks[image],bank=bank,x=x,y=y,w=w,h=h,opaque=opaque,patterns=sorted(patterns[image]))
            new+=1
    image_stats.append(dict(image=image,valid=valid,existing=seen,new_unique=new,rectangles=len(rects),width=width,height=height))
    if number%50==0:(OUT/'animation_inventory_progress.json').write_text(json.dumps(dict(images=number,total_images=len(images),new_unique=len(novel),seconds=round(time.time()-started,1))))
result=dict(images=len(images),candidate_parts=total,already_registered=covered,new_unique_parts=len(novel),new_area=sum(p['w']*p['h'] for p in novel.values()),invalid_rectangles=len(invalid),empty=empty,parts=list(novel.values()),invalid=invalid,image_stats=image_stats,known_index_bindings=known)
(OUT/'animation_inventory.json').write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('parts','invalid','image_stats','known_index_bindings')}))
