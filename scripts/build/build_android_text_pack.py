"""Android pack of the Korean bitmap-glyph recognition tables (android_pack/text.pack).

Same tables as emulator/hd_fonts.FontRenderer:
  full     12x12 window, key = packbits of the mask (18 bytes)      text_patterns keys/characters
  narrow   12x8  window (12 bytes)                                    narrow_keys/narrow_characters
  compact  8x8   ((a==14)|(a==15)) packbits (8 bytes)               hud_glyphs
  hud      16x8  ink a>=13, opaque a>0 (16+16 bytes, pattern order) battle_hud_glyphs indices
  label    16x16 a>0 (32 bytes), names 'HP','EN'                     battle_hud_glyphs labels
  forecast 16x16 ink a>1, opaque a>0 (32+32 bytes, pattern order)   forecast_glyphs

  b'SRWHDTX1' then 6 sections: u32 count, u32 keybytes, count x (key bytes, u32 codepoint[4] (0-padded))

  py -3.11 -X utf8 scripts/build/build_android_text_pack.py
"""
import struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np

F=ROOT/'graphics/fonts'


def cps(s):
    c=[ord(ch) for ch in str(s)][:4];return c+[0]*(4-len(c))


def section(rows,size):
    out=struct.pack('<II',len(rows),size)
    for key,s in rows:
        assert len(key)==size,(len(key),size);out+=key+struct.pack('<4I',*cps(s))
    return out


def main():
    with np.load(F/'text_patterns.npz',allow_pickle=False) as s:
        full=[(k.tobytes(),c) for k,c in zip(s['keys'],s['characters'])]
        narrow=[(k.tobytes(),c) for k,c in zip(s['narrow_keys'],s['narrow_characters'])]
    with np.load(F/'hud_glyphs.npz') as s:
        compact={np.packbits((a==14)|(a==15)).tobytes():str(c) for a,c in zip(s['indices'],s['characters'])}
        compact=sorted(compact.items())
    with np.load(F/'battle_hud_glyphs.npz') as s:
        hud=[(np.packbits(a>=13).tobytes()+np.packbits(a>0).tobytes(),c) for a,c in zip(s['indices'],s['characters'])]
        labels={np.packbits(a>0).tobytes():str(c) for a,c in zip(s['labels'],s['label_names'])}
        labels=sorted(labels.items())
    forecast=[]
    if (F/'forecast_glyphs.npz').exists():
        with np.load(F/'forecast_glyphs.npz',allow_pickle=False) as s:
            forecast=[(np.packbits(a>1).tobytes()+np.packbits(a>0).tobytes(),c) for a,c in zip(s['indices'],s['characters'])]
    data=b'SRWHDTX1'+section(full,18)+section(narrow,12)+section(compact,8)+section(hud,32)+section(labels,32)+section(forecast,64)
    (ROOT/'android_pack/text.pack').write_bytes(data)
    print('text.pack',len(data),'bytes: full',len(full),'narrow',len(narrow),'compact',len(compact),'hud',len(hud),'labels',len(labels),'forecast',len(forecast))


if __name__=='__main__':main()
