"""Compile recognition tables once; the player never opens development ROMs."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import unicodedata
import numpy as np
from hd_core import ROOT
from hd_fonts import FontRenderer

def main():
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();original=(ROOT/'inputs/SRWW_Japan.nds').read_bytes();glyphs={};narrow={}
    for off in range(0x445fc,0x4d530,26):
        try:ch=original[off:off+2].decode('cp932')
        except UnicodeError:continue
        normalized=unicodedata.normalize('NFKC',ch);ch=normalized if len(normalized)==1 else ch
        if ch=='・':ch='·'
        # Kanji the Korean script kept (改 in unit names) are read as well; the
        # renderer leaves any the HD font cannot draw as native.
        if len(ch)==1 and (ch.isascii() or unicodedata.category(ch)[0] in 'PS' or '一'<=ch<='鿿'):
            data=rom[off+2:off+26];pixels=np.unpackbits(np.frombuffer(data,dtype='uint8')).reshape(12,16)
            FontRenderer._add(narrow if not pixels[:,8:].any() else glyphs,data,ch,8 if not pixels[:,8:].any() else 12)
    chars=[bytes((a,b)).decode('cp949') for a in range(0xb0,0xc9) for b in range(0xa1,0xff)]
    for i,ch in enumerate(chars):
        off=0x4d530+i*26;FontRenderer._add(glyphs,rom[off+2:off+26],ch)
    # After the Hangul block the Japanese kanji remain in JIS order. A slot
    # whose bitmap is unchanged keeps the Japanese code; slots the patch
    # replaced are known only where seen on screen (改, a unit-name suffix).
    patched={2350:'改'};misses=0
    for i in range(len(chars),len(chars)+8000):
        off=0x4d530+i*26
        if off+26>len(original):break
        if i in patched:FontRenderer._add(glyphs,rom[off+2:off+26],patched[i]);continue
        if rom[off+2:off+26]!=original[off+2:off+26]:continue
        try:ch=original[off:off+2].decode('cp932')
        except UnicodeError:
            misses+=1
            if misses>4:break
            continue
        misses=0
        if len(ch)==1 and '一'<=ch<='鿿':FontRenderer._add(glyphs,rom[off+2:off+26],ch)
    glyphs={k:v for k,v in glyphs.items() if v is not None};narrow={k:v for k,v in narrow.items() if v is not None}
    keys=np.array(sorted(glyphs),dtype='V18');narrow_keys=np.array(sorted(narrow),dtype='V12')
    path=ROOT/'graphics/fonts/text_patterns.npz'
    np.savez_compressed(path,keys=keys,characters=np.array([glyphs[k.tobytes()] for k in keys]),narrow_keys=narrow_keys,narrow_characters=np.array([narrow[k.tobytes()] for k in narrow_keys]))
    print('Compiled',len(keys),len(narrow_keys),'glyphs;',path.stat().st_size,'bytes')

if __name__=='__main__':main()
