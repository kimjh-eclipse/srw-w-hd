"""Find cut-in pictures (BG layers) that attacks show WITHOUT HD.

Plays attack-start states (unit review cache) with HD on and, every STEP frames, looks at
each enabled BG layer: covered when the core matched an HD cut-in on it (cutin_layers row
with that layer) or an HD background. An uncovered layer that fills a large part of the
picture area (rows above the text box) is identified by ROM IMG id (live tile bytes vs the
IMG tile index of build_cutin_request_packet). Per IMG the frame where it is most visible
is kept, so a request packet can be built from it.

  py -3.11 -X utf8 scripts/verify/scan_uncovered_cutins.py [--limit N] [--procs 5]
Output: test_current/parts/cutin_requests/_scan/scan.json
"""
import argparse,ctypes as C,hashlib,json,os,pickle,sys
from pathlib import Path
from multiprocessing import Pool
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))

ROM=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
STARTS=ROOT/'test_current/gui/unit_review/attack_starts'
OUT=ROOT/'test_current/parts/cutin_requests/_scan'
STEP=6;FRAMES=2400;MIN_VISIBLE=4000   # pixels of the 256x128 picture area (32768)
_core=None;_index=None


def init():
    global _core,_index
    from hd_core import Core
    d=OUT/f'saves_{os.getpid()}';d.mkdir(parents=True,exist_ok=True)
    _core=Core(ROM,enabled=True,demo=True,user_dir=d)
    _index=pickle.loads((ROOT/'test_current/parts/cutin_requests/_img_tile_index.pkl').read_bytes())


def identify(info):
    maps=C.create_string_buffer(info[5]*info[6]//32);_core.api.retro_srw_copy_vram(info[1],maps,len(maps))
    tiles=C.create_string_buffer(65536);_core.api.retro_srw_copy_vram(info[2],tiles,len(tiles))
    bpp=8 if info[0]&0x80 else 4;size=32 if bpp==4 else 64;table=_index['idx4' if bpp==4 else 'idx8']
    used={int(e)&0x3ff for e in np.frombuffer(maps.raw,dtype='<u2')};hits={};total=0
    for i in used:
        t=tiles.raw[i*size:(i+1)*size]
        if len(t)<size or t.count(0)==size:continue
        total+=1
        for r in table.get(hashlib.sha1(t).digest()[:10],()):hits[r]=hits.get(r,0)+1
    return total,sorted(hits.items(),key=lambda kv:-kv[1])[:3]


def scan(state):
    found={}
    try:
        _core.load(state)
        for f in range(FRAMES):
            if not _core.run():continue
            _core.audio.clear()
            if f%STEP:continue
            ids=np.asarray(_core.ids)[:128]
            covered={int(r[5]) for r in _core.cutin_layers if int(r[0])>0}|{int(b[3]) for b in _core.backgrounds}
            for layer in range(4):
                info=_core.bg_layout[layer]
                if not info[7] or layer in covered:continue
                vis=int((ids==layer).sum())
                if vis<MIN_VISIBLE:continue
                total,top=identify(info)
                for img,n in top:
                    if n<max(8,total*.3):continue
                    k=str(img);cur=found.get(k)
                    if cur is None or vis>cur['visible']:
                        found[k]=dict(image=img,state=str(Path(state).relative_to(ROOT)).replace('\\','/'),frame=f+1,layer=layer,visible=vis,matched=n,live_tiles=total)
    except Exception as e:
        return str(state),dict(error=str(e)[:200])
    return str(state),found


def main():
    p=argparse.ArgumentParser();p.add_argument('--limit',type=int,default=0);p.add_argument('--procs',type=int,default=5);p.add_argument('--since',type=float,default=0,help='only states modified after this unix time');p.add_argument('--out',default='scan.json');a=p.parse_args()
    states=sorted(STARTS.glob('*.state'))
    if a.since:states=[s for s in states if s.stat().st_mtime>a.since]
    if a.limit:states=states[:a.limit]
    OUT.mkdir(parents=True,exist_ok=True);images={};errors={}
    with Pool(a.procs,initializer=init) as pool:
        for n,(s,res) in enumerate(pool.imap_unordered(scan,states),1):
            if 'error' in res:errors[s]=res['error'];continue
            for k,v in res.items():
                cur=images.setdefault(k,dict(best=v,scenes=[]))
                cur['scenes'].append(Path(v['state']).stem+f"@{v['frame']}")
                if v['visible']>cur['best']['visible']:cur['best']=v
            if n%25==0:
                print('states',n,'/',len(states),'images',len(images),flush=True)
                (OUT/a.out).write_text(json.dumps(dict(states=n,images=images,errors=errors),indent=1),encoding='utf-8')
    (OUT/a.out).write_text(json.dumps(dict(states=len(states),images=images,errors=errors),indent=1),encoding='utf-8')
    print('done states',len(states),'uncovered images',len(images),'errors',len(errors))


if __name__=='__main__':main()
