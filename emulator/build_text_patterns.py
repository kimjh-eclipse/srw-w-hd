"""Compile recognition tables once; the player never opens development ROMs."""
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
        if len(ch)==1 and (ch.isascii() or unicodedata.category(ch)[0] in 'PS'):
            data=rom[off+2:off+26];pixels=np.unpackbits(np.frombuffer(data,dtype='uint8')).reshape(12,16)
            FontRenderer._add(narrow if not pixels[:,8:].any() else glyphs,data,ch,8 if not pixels[:,8:].any() else 12)
    chars=[bytes((a,b)).decode('cp949') for a in range(0xb0,0xc9) for b in range(0xa1,0xff)]
    for i,ch in enumerate(chars):
        off=0x4d530+i*26;FontRenderer._add(glyphs,rom[off+2:off+26],ch)
    glyphs={k:v for k,v in glyphs.items() if v is not None};narrow={k:v for k,v in narrow.items() if v is not None}
    keys=np.array(sorted(glyphs),dtype='V18');narrow_keys=np.array(sorted(narrow),dtype='V12')
    path=ROOT/'graphics/fonts/text_patterns.npz'
    np.savez_compressed(path,keys=keys,characters=np.array([glyphs[k.tobytes()] for k in keys]),narrow_keys=narrow_keys,narrow_characters=np.array([narrow[k.tobytes()] for k in narrow_keys]))
    print('Compiled',len(keys),len(narrow_keys),'glyphs;',path.stat().st_size,'bytes')

if __name__=='__main__':main()
