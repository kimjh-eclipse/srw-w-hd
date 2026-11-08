"""Extract every palette/IMG/PAT sprite package without changing the ROM."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import sys,json,struct,math,zlib
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/all_units';OUT.mkdir(exist_ok=True)
rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
candidates=json.loads((ROOT/'test_current/rom_catalog/sprite_packages.json').read_text());packages=[];rejected=[]
# Some unit archives store IMG/PLT/PAT instead of PLT/IMG/PAT. Discover
# both orders from headers rather than silently excluding the former.
rows=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];byid={r['id']:r for r in rows}
present={r['id'] for r in candidates}
for r in rows:
    i=r['id']
    if r['kind']=='IMG' and byid.get(i+1,{}).get('kind')=='PLT' and byid.get(i+2,{}).get('kind')=='PAT' and i not in present:
        candidates.append(dict(r,palette_resource=i+1,pattern_resource=i+2));present.add(i)
candidates.sort(key=lambda r:r['id'])
for record in candidates:
    i=record['id'];palette_id=record.get('palette_resource',i-1);pattern_id=record.get('pattern_resource',i+1)
    raw=resource(i);pat=resource(pattern_id);palette=resource(palette_id)
    n=struct.unpack_from('<I',pat,4)[0]
    if n>10000 or 8+n*4>len(pat):rejected.append([i,'PAT header']);continue
    poses=[];rectangles=set()
    try:
        for j in range(n):
            at=struct.unpack_from('<I',pat,8+j*4)[0];count=struct.unpack_from('<H',pat,at)[0]
            pose=[];cursor=at+2
            for _ in range(count):
                flags=struct.unpack_from('<H',pat,cursor)[0];cursor+=2;x=y=0
                if flags&0x2000:x,y=struct.unpack_from('<hh',pat,cursor);cursor+=4
                tile=struct.unpack_from('<H',pat,cursor)[0]&4095;cursor+=2
                if flags&0x4000:cursor+=4
                if flags&0x8000:cursor+=2
                w=8<<(flags&3);h=8<<((flags>>2)&3);u=tile%32*8;v=tile//32*8
                if u+w>record['w'] or v+h>record['h']:continue
                rectangles.add((u,v,w,h));pose.append(dict(flags=flags,x=x,y=y,tile=tile,u=u,v=v,w=w,h=h))
            poses.append(pose)
    except (ValueError,struct.error):rejected.append([i,'PAT records']);continue
    if not rectangles:rejected.append([i,'no in-bounds parts']);continue
    indexed=g.pixels(raw);pal=np.array(g.palette(palette),dtype='uint8');rgba=pal[indexed].copy();rgba[:,:,3]=(indexed!=0).astype('uint8')*255
    rgba[indexed==0,:3]=0
    image=Image.fromarray(rgba);image.save(OUT/f'unit_{i}_native.png')
    parts=[]
    for u,v,w,h in sorted(rectangles,key=lambda r:(r[1],r[0],r[2],r[3])):
        indices=indexed[v:v+h,u:u+w].copy();colors=np.frombuffer(palette[8:],'<u2').astype('uint32')
        encoded=np.where(indices!=0,colors[indices]|0x8000,0).astype('<u2')
        if np.count_nonzero(encoded)<3:continue
        index_data=np.where(indices!=0,indices.astype('uint16')|0x8000,0).astype('<u2')
        parts.append(dict(x=u,y=v,w=w,h=h,hash=zlib.crc32(encoded.tobytes())^(w<<16)^h,index_hash=zlib.crc32(index_data.tobytes())^(w<<16)^h))
    if not parts:continue
    packages.append(dict(resource=i,palette_resource=palette_id,pattern_resource=pattern_id,width=record['w'],height=record['h'],palette_rgb=pal[:,:3].tolist(),parts=parts,poses=poses))
    # Independent native assembly is a review aid, not the replacement asset.
    pose=next((p for p in poses if p),[]);assembled=Image.new('RGBA',(256,192))
    for p in reversed(pose):
        piece=image.crop((p['u'],p['v'],p['u']+p['w'],p['v']+p['h']))
        assembled.alpha_composite(piece,(128+p['x'],100+p['y']))
    assembled.save(OUT/f'unit_{i}_pose.png')
manifest=dict(packages=packages,rejected=rejected,total_parts=sum(len(p['parts']) for p in packages))
(OUT/'catalog.json').write_text(json.dumps(manifest,indent=2))
for page in range(math.ceil(len(packages)/48)):
    sheet=Image.new('RGB',(1536,8*126),(30,34,42));draw=ImageDraw.Draw(sheet)
    for j,p in enumerate(packages[page*48:(page+1)*48]):
        im=Image.open(OUT/f"unit_{p['resource']}_pose.png").resize((192,144));x=j%8*192;y=j//8*126
        sheet.paste(im,(x,y-20),im);draw.text((x+3,y+105),str(p['resource']),fill='white')
    sheet.save(OUT/f'review_{page:02}.png')
print(json.dumps(dict(packages=len(packages),parts=manifest['total_parts'],rejected=len(rejected))))
