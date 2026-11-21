"""Android HD pack for pilot portraits (android_pack/portraits.pack).

Same lookup as emulator/hd_portraits.PortraitRenderer: key = zlib.crc32 of (native[y+2:y+46,5:48] >> 3)
(RGB bytes) = item content_crc32 (else crc32); then the exact reference check against portrait_mask
(56x48, polygon area). Art = _prepare_art_from_source at 4x (MAX_WIDTH 1024), WebP lossless.

  header b'SRWHDPT1', u32 n
  n x (u32 key, i32 x, w, h, u64 off, u32 len, u32 has_ref)  then for has_ref: 56*48 bytes mask + 56*48*3 rgb5
  blobs

  py -3.11 -X utf8 scripts/build/build_android_portrait_pack.py
"""
import io,json,struct,sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw

G=ROOT/'graphics';OUT=ROOT/'android_pack'


def art_job(item):
    import hd_portraits
    hd_portraits.MAX_WIDTH=1024;hd_portraits.MAX_HEIGHT=768
    art=hd_portraits._prepare_art_from_source(item)
    b=io.BytesIO();art.save(b,'WEBP',lossless=True,exact=True,method=4);return b.getvalue()


def reference(item):
    path=item.get('portrait_mask')
    if not path:return None
    rgba=np.asarray(Image.open(G/path).convert('RGBA'))
    area=Image.new('L',(56,48));ImageDraw.Draw(area).polygon([(4,1),(48,1),(52,5),(52,47),(4,47)],fill=255)
    mask=(rgba[:,:,3]>0)&(np.asarray(area)>0)
    return mask.astype('uint8').tobytes()+(rgba[:,:,:3]>>3).astype('uint8').tobytes()


def main():
    items=json.loads((G/'portraits/library.json').read_text())['portraits']
    items=[i for i in items if (G/i['path']).exists()]
    with ProcessPoolExecutor(8) as ex:blobs=list(ex.map(art_job,items,chunksize=8))
    refs=[reference(i) for i in items]
    head=12+len(items)*32+sum(len(r) for r in refs if r);pos=head
    with open(OUT/'portraits.pack','wb') as f:
        f.write(b'SRWHDPT1'+struct.pack('<I',len(items)))
        for i,b,r in zip(items,blobs,refs):
            x,_,w,h=i['rectangle']
            f.write(struct.pack('<IiiiQII',int(i.get('content_crc32',i['crc32'])),x,w,h,pos,len(b),1 if r else 0));pos+=len(b)
            if r:f.write(r)
        assert f.tell()==head,(f.tell(),head)
        for b in blobs:f.write(b)
    print('portraits',len(items),'pack',round(pos/1e6,1),'MB')


if __name__=='__main__':main()
