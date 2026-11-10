"""Read W's actual unit/weapon indirection tables; never infer names from art.

Offsets are verified against the ARM9 accessors at ROM 0x2072c (unit name),
0x24818 (weapon name), and 0x25898 (unit IMG). ROMs remain read-only.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
from collections import Counter, defaultdict
import json, struct, unicodedata, zlib
from functools import lru_cache
import numpy as np
from scripts.assets import srw_graphics as g

ROOT=PROJECT_ROOT
UNIT_MAP=0x6f8c0
UNIT_STATS=0x763e0
UNIT_GFX=0x716d8
WEAPON_MAP=0x708c0
WEAPON_STATS=0x80d58
PILOT_MAP=0x70074
PILOT_STATS=0x90b0c
PILOT_COUNT=(WEAPON_MAP-PILOT_MAP)//4
UNIT_COUNT=493
WEAPON_COUNT=(UNIT_GFX-WEAPON_MAP)//2

def catalog():
    original=(ROOT/'inputs/SRWW_Japan.nds').read_bytes()
    korean=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes()
    chars=[bytes((a,b)).decode('cp949') for a in range(0xb0,0xc9) for b in range(0xa1,0xff)]
    glyphs={original[0x4d530+i*26:0x4d532+i*26]:ch for i,ch in enumerate(chars)}
    def text(rom,ptr,translated=False):
        off=ptr-0x1ffc000
        if not 0x4000<=off<0xab238:raise ValueError(hex(ptr))
        raw=rom[off:rom.index(0,off)]
        if not translated:return unicodedata.normalize('NFKC',raw.decode('cp932'))
        result=[];i=0
        while i<len(raw):
            if raw[i]<128:result.append(chr(raw[i]));i+=1;continue
            pair=raw[i:i+2];result.append(glyphs.get(pair,pair.decode('cp932',errors='replace')));i+=2
        return unicodedata.normalize('NFKC',''.join(result))
    def names(off):
        return {'name_ja':text(original,struct.unpack_from('<I',original,off)[0]),
                'name_ko':text(korean,struct.unpack_from('<I',korean,off)[0],True)}
    records=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records']
    kinds={r['id']:r['kind'] for r in records}
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text())
    rgb={b['hash'] for b in library['bindings'] if b.get('rgb_enabled',True) and not b.get('disabled')}
    indexed={b.get('index_hash') for b in library['bindings'] if b.get('dynamic_palette') and b.get('indexed_safe',True) and not b.get('disabled')}
    indexed-=set(library.get('indexed_collision_keys',[]))
    offsets=g.archive(korean)
    @lru_cache(maxsize=256)
    def resource(i):return g.decompress(korean[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    @lru_cache(maxsize=512)
    def primary_parts(img,palette,pattern):
        if kinds.get(img)!='IMG' or kinds.get(palette)!='PLT' or kinds.get(pattern)!='PAT':return dict(status='no_primary_triplet')
        a=g.pixels(resource(img));palraw=resource(palette)
        pal=np.frombuffer(palraw[8:],dtype='<u2');pat=resource(pattern)
        count=struct.unpack_from('<I',pat,4)[0];seen=set();missing=[];invalid=[];small=0
        for pose in range(count):
            off=struct.unpack_from('<I',pat,8+pose*4)[0];n=struct.unpack_from('<H',pat,off)[0];off+=2
            for _ in range(n):
                flags=struct.unpack_from('<H',pat,off)[0];off+=2
                if flags&0x2000:off+=4
                tile=struct.unpack_from('<H',pat,off)[0];off+=2
                if flags&0x4000:off+=4
                if flags&0x8000:off+=2
                w=8<<(flags&3);h=8<<((flags>>2)&3);x=(tile&4095)%32*8;y=(tile&4095)//32*8;bank=tile>>12
                key=(x,y,w,h,bank)
                if key in seen:continue
                seen.add(key)
                if x+w>a.shape[1] or y+h>a.shape[0]:invalid.append(list(key));continue
                pixels=a[y:y+h,x:x+w];opaque=int(np.count_nonzero(pixels))
                if not opaque:continue
                ii=np.where(pixels,pixels.astype('uint16')|0x8000,0).astype('<u2')
                ih=zlib.crc32(ii.tobytes())^(w<<16)^h
                bankpal=pal[bank*16:(bank+1)*16]
                if len(bankpal)<=int(pixels.max()):bankpal=pal[:16]
                if len(bankpal)<=int(pixels.max()):invalid.append(list(key));continue
                cc=np.where(pixels,bankpal[pixels]|0x8000,0).astype('<u2');rh=zlib.crc32(cc.tobytes())^(w<<16)^h
                if ih not in indexed and rh not in rgb:
                    if opaque<16:small+=1
                    missing.append(dict(x=x,y=y,w=w,h=h,bank=bank,opaque=opaque,index_hash=ih,hash=rh))
        return dict(status='audited',unique_rectangles=len(seen),unmapped_parts=missing,out_of_bounds=invalid,unmapped_tiny_parts=small)
    registered=defaultdict(list)
    for bid,b in enumerate(library['bindings'],1):
        if not b.get('disabled') and 'resource' in b:registered[b['resource']].append(bid)
    primary=json.loads((ROOT/'graphics/all_units/installed.json').read_text())
    for row in primary['coverage']:registered[row['resource']].extend(row['bindings'])
    pilots=[]
    for pid in range(PILOT_COUNT):
        stats,slot=struct.unpack_from('<hh',original,PILOT_MAP+pid*4)
        pilots.append(dict(pilot_id=pid,stats_id=stats,roster_slot=slot,**names(PILOT_STATS+stats*168)))
    units=[]
    for uid in range(UNIT_COUNT):
        stats,secondary=struct.unpack_from('<hh',original,UNIT_MAP+uid*4)
        assert 0<=stats<493
        off=UNIT_STATS+88*stats;gfx=UNIT_GFX+40*uid
        start,end=struct.unpack_from('<HH',original,gfx+32)
        img=struct.unpack_from('<H',original,gfx+8)[0]
        small=struct.unpack_from('<H',original,gfx+4)[0]
        palette,pattern=struct.unpack_from('<HH',original,gfx+10)
        series_ptr=struct.unpack_from('<I',original,off+12)[0]
        pilot_id=struct.unpack_from('<H',original,off+38)[0]
        pilot=pilots[pilot_id] if pilot_id<PILOT_COUNT else None
        units.append(dict(unit_id=uid,stats_id=stats,secondary_map_id=secondary,**names(off),
                          default_pilot_id=pilot_id if pilot else None,
                          default_pilot_name_ja=pilot['name_ja'] if pilot else None,
                          default_pilot_roster_slot=pilot['roster_slot'] if pilot else None,
                          default_pilot_ids=[p for p in struct.unpack_from('<6H',original,off+38) if p<PILOT_COUNT],
                          series_ja=text(original,series_ptr),
                          primary_image=img if kinds.get(img)=='IMG' else None,
                          secondary_image=small if kinds.get(small)=='IMG' else None,
                          resource_start=start if start!=65535 else None,
                          resource_end=end if end!=65535 else None,
                          registered_primary_bindings=len(set(registered[img])),
                          primary_part_coverage=primary_parts(img,palette,pattern),
                          weapon_start=struct.unpack_from('<H',original,off+50)[0],
                          weapon_count=original[off+52],
                          hp=struct.unpack_from('<I',original,off+16)[0],
                          en=struct.unpack_from('<H',original,off+28)[0],
                          actual_game_replay_verified=False))
    weapons=[]
    for wid in range(WEAPON_COUNT):
        stats=struct.unpack_from('<h',original,WEAPON_MAP+wid*2)[0]
        assert 0<=stats<2000,(wid,stats)
        off=WEAPON_STATS+stats*36
        weapons.append(dict(weapon_id=wid,stats_id=stats,**names(off),
                            attack=struct.unpack_from('<H',original,off+12)[0],
                            actual_game_replay_verified=False))
    # ARM9 accessor 0x2090c reads the signed byte at unit-stat offset 52.
    # This is the actual list length, independent of the next unit's list.
    for u in units:
        first=u['weapon_start'];last=first+u['weapon_count']
        assert not u['weapon_count'] or last<=WEAPON_COUNT,(u['unit_id'],first,last)
        u['weapon_ids']=list(range(first,last)) if u['weapon_count'] else []
        u['weapon_range_verified']=True
    return dict(unit_count=len(units),weapon_count=len(weapons),
                series_counts=dict(Counter(u['series_ja'] for u in units)),
                scope='ROM-defined records, including enemy/stat/transform variants; not unique designs',
                units_with_unmapped_primary_parts=[u['unit_id'] for u in units if u['primary_part_coverage'].get('unmapped_parts')],
                units_with_primary_bounds_issues=[u['unit_id'] for u in units if u['primary_part_coverage'].get('out_of_bounds')],
                pilots=pilots,units=units,weapons=weapons)

def main():
    result=catalog();out=ROOT/'test_current/parts/named_unit_catalog.json'
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ('units','weapons','pilots')},ensure_ascii=False))

if __name__=='__main__':main()
