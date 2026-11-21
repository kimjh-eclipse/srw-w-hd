"""Android pack for palette-indexed (recoloured) non-robot parts: HUD digits, effects (android_pack/indexed.pack).

Registration follows hd_core.py: dynamic_palette, indexed_safe, not disabled, index_hash not in
indexed_collision_keys, robot bindings left out (SRWW_NO_RECOLOUR default: robots never recoloured).
Only bindings whose texture is in parts.pack are kept (Android cannot prepare art at run time).
For each, the recolour inputs of hd_parts.PartsRenderer.sprite: source palette (palette_source_rgb,
else original_palette_rgb, else library source_palette_rgb), the original palette (no-op check),
the slots the part uses (used_palette_indices) and the exact RGB hash.

  textures: android_pack/parts_indexed.pack, same format as parts.pack (key field = index_hash),
  for the bindings not already in parts.pack (index-only bindings have rgb_enabled false).

  b'SRWHDIX1', u32 n, n x (u32 index_hash, u32 binding, u32 rgb_hash, u16 used_mask, u16 pad,
                         u8 source[16][3], u8 original[16][3], u8 has_original, u8 pad[3])

  py -3.11 -X utf8 scripts/build/build_android_indexed_pack.py
"""
import os,sqlite3,struct,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
import numpy as np

OUT=ROOT/'android_pack'


def pal16(p):
    a=np.zeros((16,3),dtype='uint8')
    if p is not None and len(p):
        v=np.clip(np.rint(np.asarray(p,dtype='float32')[:16]),0,255).astype('uint8');a[:len(v)]=v
    return a


def main():
    os.environ.setdefault('SRWW_QUARANTINE','1')
    from hd_parts import PartsRenderer
    from parts_catalog import load_parts_library
    from robot_sprite_switch import robot_ids
    r=PartsRenderer(async_prepare=False);B=r.bindings
    library,digest=load_parts_library(ROOT/'graphics/kazuma_parts_library.json')
    blocked=set(library.get('indexed_collision_keys',[]))
    robots=robot_ids(library['bindings'],digest)
    # bindings with a texture in parts.pack
    data=(OUT/'parts.pack').read_bytes();n=struct.unpack_from('<I',data,8)[0]
    packed={struct.unpack_from('<I',data,12+i*28)[0] for i in range(n)}
    rows=[];skipped=0;extra=[];tex={}
    db=sqlite3.connect(f"file:{(ROOT/'graphics/parts_baked.sqlite').as_posix()}?mode=ro",uri=True)
    for i,b in enumerate(B,1):
        if not (b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled') and b.get('index_hash') not in blocked):continue
        if i in robots:continue
        if i not in packed:
            src_b=b.get('source_binding',i)
            if src_b in r.quarantine:skipped+=1;continue
            if src_b not in tex:
                s_=B[src_b-1]
                try:key=r.texture_key(src_b,s_['w'],s_['h'])
                except Exception:key=None
                tex[src_b]=db.execute('select pixels from textures where key=?',(key,)).fetchone() if key else None
            if tex[src_b] is None:skipped+=1;continue
            extra.append((i,int(b['index_hash']),src_b,b['w'],b['h']))
        src=b.get('palette_source_rgb',b.get('original_palette_rgb',r.source_palette))
        src=np.asarray(src,dtype='float32')
        used=r.used_palette_indices(i,src,b)
        mask=0
        if used is not None:
            for u in np.asarray(used).tolist():
                if 0<u<16:mask|=1<<int(u)
        orig=b.get('original_palette_rgb')
        rows.append(struct.pack('<IIIHH',int(b['index_hash']),i,int(b.get('hash') or 0),mask,0)+pal16(src).tobytes()+pal16(orig).tobytes()+bytes([1 if orig is not None else 0,0,0,0]))
    used_src=sorted({e[2] for e in extra});pos=12+28*len(extra);offs={}
    for s_ in used_src:offs[s_]=(pos,len(tex[s_][0]));pos+=len(tex[s_][0])
    with open(OUT/'parts_indexed.pack','wb') as f:
        f.write(b'SRWHDPK1'+struct.pack('<I',len(extra)))
        for b_,h,s_,w,hh in extra:o,l=offs[s_];f.write(struct.pack('<IIIHHQI',b_,h,s_,w,hh,o,l))
        for s_ in used_src:f.write(tex[s_][0])
    print('extra textures',len(extra),'bindings',len(used_src),'sources',round(pos/1e6),'MB')
    (OUT/'indexed.pack').write_bytes(b'SRWHDIX1'+struct.pack('<I',len(rows))+b''.join(rows))
    print('indexed parts',len(rows),'(no texture in pack:',skipped,') robots excluded',len(robots))


if __name__=='__main__':main()
