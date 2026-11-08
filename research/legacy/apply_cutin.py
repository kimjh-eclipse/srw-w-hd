"""Encode the approved redraw into W's existing cut-in resource slots.

This replaces art at the native DS resolution; it does not add FHD rendering.
Input artwork is only resized/quantized for the game's tile/palette format.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import hashlib,json,struct,zlib
import numpy as np
from PIL import Image
from scripts.assets.srw_graphics import ROOT, BASE, archive, decompress, compress

def prepare():
    art=ROOT/'graphics/kazuma_cutin_hd.png'
    image=Image.open(art).convert('RGBA').resize((256,192),Image.Resampling.LANCZOS)
    rgba=np.asarray(image);opaque=rgba[:,:,3]>=128
    sample=Image.fromarray(rgba[:,:,:3][opaque].reshape(1,-1,3))
    palette_image=sample.quantize(colors=15,method=Image.Quantize.MEDIANCUT)
    indices=np.asarray(image.convert('RGB').quantize(palette=palette_image,dither=Image.Dither.NONE)).copy()+1
    indices[~opaque]=0
    canvas=np.zeros((200,256),dtype='uint8');canvas[:192]=indices
    rgb=np.asarray(palette_image.getpalette()[:45],dtype='uint8').reshape(15,3)
    pal=[0x2b0e]+[int(c[0]>>3)|int(c[1]>>3)<<5|int(c[2]>>3)<<10 for c in rgb]
    blank=np.zeros((8,8),dtype='uint8');tiles=[blank];lookup={blank.tobytes():0};screen=np.zeros((25,32),dtype='<u2')
    for y in range(25):
        for x in range(32):
            tile=canvas[y*8:y*8+8,x*8:x*8+8]
            key=tile.tobytes()
            if key not in lookup:
                idx=len(tiles);tiles.append(tile.copy())
                for a,flags in [(tile,0),(tile[:,::-1],1024),(tile[::-1],2048),(tile[::-1,::-1],3072)]:
                    lookup.setdefault(a.tobytes(),idx|flags)
            screen[y,x]=lookup[key]
    assert len(tiles)<=512,len(tiles)
    unique=len(tiles)
    tiles.extend([blank]*(512-len(tiles)))
    flat=np.stack(tiles).reshape(-1)
    packed=(flat[::2]|flat[1::2]<<4).astype('uint8').tobytes()
    return b'IMG\0'+struct.pack('<HH',32,16)+packed,screen,pal,unique

def patch_bytes(source):
    rom=bytearray(source);offsets=archive(rom)
    fat_off,fat_size=struct.unpack_from('<II',rom,0x48)
    rows=[struct.unpack_from('<II',rom,fat_off+i*8) for i in range(fat_size//8)]
    fid=next(i for i,(a,b) in enumerate(rows) if a==BASE)
    old_start,old_end=rows[fid];old=bytes(rom[old_start:old_end])
    image,screen,pal,unique=prepare();encoded_image=compress(image);replacements={}
    for i in range(25111,25127):replacements[i]=encoded_image
    for i in range(25127,25143):
        raw=decompress(old[offsets[i]:offsets[i+1]])
        assert raw[:4]==b'SCR\0' and raw[5]==32
        height=struct.unpack_from('<H',raw,6)[0];assert height in (24,25)
        replacements[i]=compress(raw[:8]+screen[:height].tobytes())
    for i in range(25095,25111):
        raw=bytearray(old[offsets[i]:offsets[i+1]])
        assert raw[:4]==b'PLT\0' and len(raw)==232
        struct.pack_into('<16H',raw,8,*pal);replacements[i]=bytes(raw)
    rebuilt=bytearray(len(offsets)*4);new_offsets=[]
    for i,off in enumerate(offsets):
        new_offsets.append(len(rebuilt))
        block=replacements.get(i,old[off:offsets[i+1] if i+1<len(offsets) else len(old)])
        rebuilt.extend(block);rebuilt.extend(b'\0'*((-len(rebuilt))%4))
    struct.pack_into(f'<{len(offsets)}I',rebuilt,0,*new_offsets)
    if len(rebuilt)<=len(old):
        rom[old_start:old_end]=rebuilt+b'\xff'*(len(old)-len(rebuilt));new_start=old_start
    else:
        rom.extend(b'\xff'*((-len(rom))%0x200));new_start=len(rom);rom.extend(rebuilt)
        rom.extend(b'\xff'*((-len(rom))%0x200))
    struct.pack_into('<II',rom,fat_off+fid*8,new_start,new_start+len(rebuilt))
    struct.pack_into('<I',rom,0x80,len(rom))
    rom[0x14]=next(code for code in range(13) if len(rom)<=1<<(17+code))
    crc=0xffff
    for value in rom[:0x15e]:
        crc^=value
        for _ in range(8):crc=(crc>>1)^(0xa001 if crc&1 else 0)
    struct.pack_into('<H',rom,0x15e,crc)
    # All unmodified archive entries must remain byte-exact.
    for i in range(len(offsets)-1):
        if i not in replacements:
            assert old[offsets[i]:offsets[i+1]]==rebuilt[new_offsets[i]:new_offsets[i+1]]
    info=dict(artwork='graphics/kazuma_cutin_hd.png',native_display=[256,192],
              fhd_renderer=False,palette_colors=15,unique_tiles=unique,
              image_resources=list(range(25111,25127)),screen_resources=list(range(25127,25143)),
              palette_resources=list(range(25095,25111)),archive_file_id=fid,
              old_archive=[old_start,len(old)],new_archive=[new_start,len(rebuilt)],
              artwork_sha256=hashlib.sha256((ROOT/'graphics/kazuma_cutin_hd.png').read_bytes()).hexdigest())
    return bytes(rom),info

def apply_to_rom(path):
    path=Path(path);data,info=patch_bytes(path.read_bytes());path.write_bytes(data)
    (ROOT/'graphics/cutin_application.json').write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
    return info

if __name__=='__main__':
    target=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
    data,info=patch_bytes(target.read_bytes())
    # Keep this stage read-only until the actual battle verifies successfully.
    print(json.dumps(info,ensure_ascii=False,indent=2))
