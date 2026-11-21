"""Android HD pack (robot/OBJ/BG parts) from the PC baked store.

The PC player finds a part texture by a content key (sha256 over registration code and atlas
files, hd_parts.texture_key) in graphics/parts_baked.sqlite. Android cannot recompute that key,
so this exports a plain table:

  android_pack/parts.pack
    header  b'SRWHDPK1', u32 count
    entries count * (u32 binding, u32 hash, u32 source_binding, u16 w, u16 h, u64 offset, u32 length)
            sorted by binding; w,h = native size (texture is 4x); offset/length into the file of the
            texture (lossless WebP as stored) for source_binding; length 0 = no texture (stays native)
    data    WebP blobs, one per source texture
  android_pack/parts_hashes.bin   u32[len(bindings)]: hash to register per binding (0 = not registered)

Registration rule follows hd_core.py: rgb_enabled and not disabled; aliases with palette_rgb are
not registered (they need recolouring); bindings without a baked texture are not registered either.

  py -3.11 -X utf8 scripts/build/build_android_pack.py
"""
import json,os,sqlite3,struct,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT

OUT=ROOT/'android_pack'


def main():
    os.environ.setdefault('SRWW_QUARANTINE','1')
    from hd_parts import PartsRenderer
    r=PartsRenderer(async_prepare=False)
    B=r.bindings;n=len(B)
    db=sqlite3.connect(f"file:{(ROOT/'graphics/parts_baked.sqlite').as_posix()}?mode=ro",uri=True)
    OUT.mkdir(exist_ok=True)
    rows=[];sources={};missing=0;t=time.time()
    for i,spec in enumerate(B,1):
        if spec.get('disabled') or not spec.get('rgb_enabled',True) or spec.get('palette_rgb') is not None:continue
        h=int(spec.get('hash') or 0)
        if not h:continue
        src=spec.get('source_binding',i)
        if src in r.quarantine:continue
        if src not in sources:
            s=B[src-1]
            try:key=r.texture_key(src,s['w'],s['h'])
            except Exception:key=None
            row=db.execute('select w,h,pixels from textures where key=?',(key,)).fetchone() if key else None
            sources[src]=row
        if sources[src] is None:missing+=1;continue
        rows.append((i,h,src,spec['w'],spec['h']))
        if i%20000==0:print('bindings',i,'/',n,'kept',len(rows),'missing',missing,round(time.time()-t),'s',flush=True)
    used=sorted({r_[2] for r_ in rows})
    head=8+4;entry=4*3+2*2+8+4;data_off=head+entry*len(rows)
    offsets={};pos=data_off
    for s in used:
        blob=sources[s][2];offsets[s]=(pos,len(blob));pos+=len(blob)
    with open(OUT/'parts.pack','wb') as f:
        f.write(b'SRWHDPK1'+struct.pack('<I',len(rows)))
        for b,h,s,w,hh in rows:
            o,l=offsets[s];f.write(struct.pack('<IIIHHQI',b,h,s,w,hh,o,l))
        for s in used:f.write(sources[s][2])
    hashes=[0]*n
    for b,h,s,w,hh in rows:hashes[b-1]=h
    (OUT/'parts_hashes.bin').write_bytes(struct.pack(f'<{n}I',*hashes))
    print('bindings',len(rows),'textures',len(used),'missing texture',missing,'pack',round(pos/1e6),'MB')


if __name__=='__main__':main()
