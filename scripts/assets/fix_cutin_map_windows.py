"""Measure cut-in tile probes and map windows live (GPU.cpp rule) and fix library entries that
never connect because their ROM map is not 32 tiles wide (the game re-lays it in VRAM).

For each IMG id: the scene from the cut-in scan (attack-start state + frame + BG layer) is played,
the probe hash at base*32+pad+1024 (2 KiB) and the 512-entry window hash at origin base+pad/32 are
computed as GPU.cpp does. When the probe equals one of the entry's signatures and the window differs,
map_window_signature is replaced (dry run unless --apply).

  py -3.11 -X utf8 scripts/assets/fix_cutin_map_windows.py --images 22867,22870 [--apply]
"""
import argparse,ctypes as C,json,shutil,sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))


def fnv(b):
    h=2166136261
    for x in b:h=((h^x)*16777619)&0xffffffff
    return h


def maphash(e,origin,count):
    h=2166136261
    for v in e[:count]:
        v=int(v);v=(((v&1023)-origin)&1023)|(v&3072)
        h=((h^(v&255))*16777619)&0xffffffff;h=((h^(v>>8))*16777619)&0xffffffff
    return h


def main():
    p=argparse.ArgumentParser();p.add_argument('--images',required=True);p.add_argument('--apply',action='store_true');p.add_argument('--adopt',action='store_true',help='when no mode matches, add the live base probe as a signature (layer content confirmed by the scan)');a=p.parse_args()
    from hd_core import Core
    scans={}
    for f in ('scan.json','scan_new.json'):
        q=ROOT/'test_current/parts/cutin_requests/_scan'/f
        if q.exists():
            for k,v in json.loads(q.read_text(encoding='utf-8'))['images'].items():scans.setdefault(int(k),v['best'])
    path=ROOT/'graphics/cutins_library.json';lib=json.loads(path.read_text(encoding='utf-8'));changed=[]
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=True,demo=True,user_dir=ROOT/'test_current/parts/cutin_requests/_scan/saves_fix')
    try:
        for img in map(int,a.images.split(',')):
            b=scans.get(img);entry=next((c for c in lib['cutins'] if c.get('resource')==img),None)
            if not b or not entry:print(img,'no scene or no entry');continue
            core.load(ROOT/b['state']);n=0
            while n<b['frame']:
                if core.run():n+=1
                core.audio.clear()
            info=core.bg_layout[b['layer']];W,H=info[5],info[6]
            maps=C.create_string_buffer(W*H//32);core.api.retro_srw_copy_vram(info[1],maps,len(maps));e=np.frombuffer(maps.raw,dtype='<u2')
            tiles=C.create_string_buffer(65536);core.api.retro_srw_copy_vram(info[2],tiles,len(tiles));t=tiles.raw
            base=int(e[0])&1023;hit=None
            for pad in (0,64):
                for off in (1024,):
                    probe=fnv(t[base*32+pad+off:base*32+pad+off+2048])
                    if probe in entry['signatures']:hit=(pad,probe,maphash(e,base+pad//32,entry.get('map_window_entries',512)))
            if hit is None:
                probe0=fnv(t[1024:3072])
                if probe0 in entry['signatures']:hit=(0,probe0,maphash(e,0,entry.get('map_window_entries',512)))
            if hit is None:   # other GPU.cpp modes: 8192 origin, padded 512-byte, band discovery
                cands={'o8192':(fnv(t[8192:10240]),0),'padded':(fnv(t[base*32+1024:base*32+1024+512]),base)}
                bands={(int(v)&1023)>>5 for v in e[:min(4096,W*H//64)]}
                for band in sorted(bands):
                    d=t[band*1024+1024:band*1024+3072];cands[f'band{band}']=(fnv(d),band*32);cands[f'band{band}s']=(fnv(d[:512]),band*32)
                for k,(pr,org) in cands.items():
                    if pr in entry['signatures']:hit=(k,pr,maphash(e,org,entry.get('map_window_entries',512)),maphash(e,org,16));break
            if hit is None and a.adopt:
                probe=fnv(t[base*32+1024:base*32+1024+2048]);hit=('adopt',probe,maphash(e,base,entry.get('map_window_entries',512)),maphash(e,base,16))
                if a.apply:entry['signatures']=sorted(set(entry['signatures'])|{probe})
                print(img,'id',entry['id'],'adopted live probe',probe,'at base',base)
            if hit is None:print(img,'id',entry['id'],'probe does not match the entry signature (base',base,') - not a window problem');continue
            old=entry.get('map_window_signature');print(img,'id',entry['id'],'base',base,'pad',hit[0],'window live',hit[2],'library',old,'MATCH' if old==hit[2] else 'DIFFERS')
            if old!=hit[2]:
                changed.append((entry['id'],old,hit[2]))
                if a.apply:
                    if len(hit)>3:entry['map_signature']=hit[3]   # band discovery also checks the 16-entry prefix
                    entry['map_window_signature']=hit[2];entry['map_window_entries']=entry.get('map_window_entries',512);entry['map_window_note']=f"measured live 11/21 at {b['state']} +{b['frame']}"
    finally:core.close()
    if a.apply and changed:
        shutil.copy2(path,ROOT/'test_current/parts/pending_install/cutins_library.before_mapwindows_20261121.json')
        path.write_text(json.dumps(lib,ensure_ascii=False,indent=1),encoding='utf-8')
    print('changed' if a.apply else 'would change',changed)


if __name__=='__main__':main()
