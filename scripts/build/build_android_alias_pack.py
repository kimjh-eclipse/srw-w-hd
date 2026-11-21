"""Android pack for palette_rgb alias parts (android_pack/parts_alias.pack) + updated parts_hashes.bin.

The main pack leaves out bindings whose spec has palette_rgb (an alias that shows the source art in
another palette): the PC player recolours them at run time (hd_parts.PartsRenderer.sprite). Left
unregistered, such a sprite counts as "native" in the core's palette-group fallback, so a whole unit
or face flips to native on the frames it appears (blinking). Here each alias is rendered once by the
PC code itself, at SCALE 4 with no flip/affine/brightness, and stored as its own texture.

Format = parts.pack (SRWHDPK1), source = binding. parts_hashes.bin gains these hashes.

  py -3.11 -X utf8 scripts/build/build_android_alias_pack.py
"""
import io,os,struct,sys,time
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT

OUT=ROOT/'android_pack'


def main():
    os.environ.setdefault('SRWW_QUARANTINE','1')
    import hd_parts
    hd_parts.SCALE=4.0
    r=hd_parts.PartsRenderer(async_prepare=False)
    B=r.bindings;n=len(B)
    hashes=list(struct.unpack(f'<{n}I',(OUT/'parts_hashes.bin').read_bytes()))
    want=[i for i,s in enumerate(B,1) if s.get('palette_rgb') is not None and s.get('rgb_enabled',True) and not s.get('disabled') and s.get('hash')]
    rows=[];blobs=[];fail=0;t=time.time();oam=bytes(1024)
    for k,i in enumerate(want,1):
        s=B[i-1]
        try:art=r.sprite([i,0,0,0,int(s['hash']),0,0,0],oam,required=True)
        except Exception as e:art=None;print('fail',i,e)
        if art is None or art.size!=(s['w']*4,s['h']*4):fail+=1;continue
        b=io.BytesIO();art.convert('RGBA').save(b,'WEBP',lossless=True,exact=True,method=4)
        rows.append((i,int(s['hash']),i,s['w'],s['h']));blobs.append(b.getvalue());hashes[i-1]=int(s['hash'])
        if k%200==0:print(k,'/',len(want),'fail',fail,round(time.time()-t),'s',flush=True)
    pos=12+28*len(rows)
    with open(OUT/'parts_alias.pack','wb') as f:
        f.write(b'SRWHDPK1'+struct.pack('<I',len(rows)))
        for (b_,h,s_,w,hh),blob in zip(rows,blobs):f.write(struct.pack('<IIIHHQI',b_,h,s_,w,hh,pos,len(blob)));pos+=len(blob)
        for blob in blobs:f.write(blob)
    (OUT/'parts_hashes.bin').write_bytes(struct.pack(f'<{n}I',*hashes))
    print('aliases',len(rows),'failed',fail,'pack',round(pos/1e6,1),'MB')


if __name__=='__main__':main()
