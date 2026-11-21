"""android_pack/effect_ids.bin: u32[] binding ids registered with retro_srw_register_effect_parts.

Same rule as hd_core.py: follow source_binding until an explicit effect_part is found; disabled -> no.

  py -3.11 -X utf8 scripts/build/build_android_effect_ids.py
"""
import struct,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
from parts_catalog import load_parts_library


def main():
    library,_=load_parts_library(ROOT/'graphics/kazuma_parts_library.json');B=library['bindings']

    def is_effect(i):
        seen=set()
        while isinstance(i,int) and 0<i<=len(B) and i not in seen:
            seen.add(i);s=B[i-1]
            if s.get('disabled'):return False
            if 'effect_part' in s:return s['effect_part'] is True
            i=s.get('source_binding')
        return False
    ids=[i for i in range(1,len(B)+1) if is_effect(i)]
    (ROOT/'android_pack/effect_ids.bin').write_bytes(struct.pack(f'<{len(ids)}I',*ids))
    print('effect ids',len(ids),'of',len(B))


if __name__=='__main__':main()
