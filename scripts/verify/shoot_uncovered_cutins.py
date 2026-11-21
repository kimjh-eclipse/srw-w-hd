"""Isolated-layer screenshots of the uncovered cut-in pictures found by scan_uncovered_cutins.py.

For every image the best frame (most visible) is replayed once per attack state: the frame is
saved, the layer alone is drawn (retro_srw_set_main_layers) and the full picture as well.
Output: test_current/parts/cutin_requests/_scan/shots/<img>_layer.png, <img>_screen.png
"""
import ctypes as C,json,os,sys
from pathlib import Path
from multiprocessing import Pool
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
sys.path.insert(0,str(ROOT/'emulator'))
ROM=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'
SCAN=ROOT/'test_current/parts/cutin_requests/_scan';SHOTS=SCAN/'shots'
_core=None


def init():
    global _core
    from hd_core import Core
    d=SCAN/f'saves_{os.getpid()}';d.mkdir(parents=True,exist_ok=True)
    _core=Core(ROM,enabled=True,demo=True,user_dir=d);_core.api.retro_srw_set_main_layers.argtypes=[C.c_uint]


def shoot(job):
    state,wants=job;tmp=SCAN/f'saves_{os.getpid()}'/'f.state';done=0
    try:
        _core.load(ROOT/state);f=0
        for frame,items in sorted(wants.items()):
            while f<frame-1:
                if _core.run():f+=1
                _core.audio.clear()
            _core.save(tmp)
            for img,layer in items:
                _core.load(tmp);_core.api.retro_srw_set_main_layers(1<<layer);_core.run();_core.audio.clear()
                Image.fromarray(np.asarray(_core.native)[:192].copy()).save(SHOTS/f'{img}_layer.png')
                _core.load(tmp);_core.api.retro_srw_set_main_layers(0x1f);_core.run();_core.audio.clear()
                Image.fromarray(np.asarray(_core.native)[:192].copy()).save(SHOTS/f'{img}_screen.png');done+=1
            _core.load(tmp);_core.api.retro_srw_set_main_layers(0x1f)
    except Exception as e:return state,str(e)[:120]
    return state,done


def main():
    SHOTS.mkdir(parents=True,exist_ok=True)
    images=json.loads((SCAN/os.environ.get('CUTIN_SCAN','scan.json')).read_text(encoding='utf-8'))['images'];jobs={}
    for k,v in images.items():
        b=v['best'];jobs.setdefault(b['state'],{}).setdefault(b['frame'],[]).append((int(k),b['layer']))
    with Pool(5,initializer=init) as pool:
        for n,(s,r) in enumerate(pool.imap_unordered(shoot,list(jobs.items())),1):
            if not isinstance(r,int):print('ERR',s,r,flush=True)
            if n%50==0:print('states',n,'/',len(jobs),flush=True)
    print('shots',len(list(SHOTS.glob('*_layer.png'))))


if __name__=='__main__':main()
