"""Whole BG-layer canvases (live VRAM map + tiles + live BG palette) for the uncovered cut-ins.

The visible 256x192 shot shows only part of a scrolling picture; Codex needs the whole
canvas. At each image's best frame the layer's map (its full width x height, text-BG screen
blocks) is decoded with the live palette; colour index 0 is transparent.
Output: test_current/parts/cutin_requests/_scan/canvas/<img>.png (+ canvas.json)
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
SCAN=ROOT/'test_current/parts/cutin_requests/_scan';OUT=SCAN/'canvas'
_core=None


def init():
    global _core
    from hd_core import Core
    d=SCAN/f'saves_{os.getpid()}';d.mkdir(parents=True,exist_ok=True)
    _core=Core(ROM,enabled=True,demo=True,user_dir=d)


def decode(info):
    cnt,mapv,tilev,_,_,W,H=info[:7];bpp=8 if cnt&0x80 else 4
    maps=C.create_string_buffer(W*H//32);_core.api.retro_srw_copy_vram(mapv,maps,len(maps))
    tiles=C.create_string_buffer(65536);_core.api.retro_srw_copy_vram(tilev,tiles,len(tiles))
    pal=np.zeros(256,dtype='<u2');_core.api.retro_srw_copy_effect_debug(None,None,pal.ctypes.data,None)
    rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],1).astype('uint8')
    e=np.frombuffer(maps.raw,dtype='<u2');t=np.frombuffer(tiles.raw,dtype='uint8')
    out=np.zeros((H,W,4),dtype='uint8');bw=W//256
    for k,v in enumerate(e):
        block=k//1024;i=k%1024;bx=(block%bw)*256 if bw else 0;by=(block//max(bw,1))*256
        x=bx+(i%32)*8;y=by+(i//32)*8
        if x>=W or y>=H:continue
        n=int(v)&0x3ff
        if bpp==4:
            raw=t[n*32:n*32+32]
            if len(raw)<32:continue
            px=np.stack([raw&15,raw>>4],1).reshape(8,8);idx=px+16*(int(v)>>12);idx[px==0]=0
        else:
            raw=t[n*64:n*64+64]
            if len(raw)<64:continue
            px=raw.reshape(8,8).astype(int);idx=px
        if v&0x400:idx=idx[:,::-1];px=px[:,::-1] if bpp==4 else idx
        if v&0x800:idx=idx[::-1];px=px[::-1] if bpp==4 else idx
        tile=np.zeros((8,8,4),dtype='uint8');tile[...,:3]=rgb[np.clip(idx,0,255)];tile[...,3]=np.where((px if bpp==4 else idx)>0,255,0)
        out[y:y+8,x:x+8]=tile
    return out


def job(item):
    state,wants=item;res={}
    try:
        _core.load(ROOT/state);f=0
        for frame,items in sorted(wants.items()):
            while f<frame:
                if _core.run():f+=1
                _core.audio.clear()
            for img,layer in items:
                info=_core.bg_layout[layer]
                if info[0]&0x80 and False:pass
                can=decode(info);Image.fromarray(can).save(OUT/f'{img}.png')
                res[img]=dict(size=[int(info[5]),int(info[6])],scroll=[int(info[3]),int(info[4])],bgcnt=hex(int(info[0])),opaque=int((can[...,3]>0).sum()))
    except Exception as e:return state,dict(error=str(e)[:120])
    return state,res


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    images=json.loads((SCAN/os.environ.get('CUTIN_SCAN','scan.json')).read_text(encoding='utf-8'))['images'];jobs={}
    for k,v in images.items():
        b=v['best'];jobs.setdefault(b['state'],{}).setdefault(b['frame'],[]).append((int(k),b['layer']))
    meta={}
    with Pool(5,initializer=init) as pool:
        for s,r in pool.imap_unordered(job,list(jobs.items())):
            if 'error' in r:print('ERR',s,r['error'],flush=True)
            else:meta.update({str(k):v for k,v in r.items()})
    (OUT/os.environ.get('CUTIN_CANVAS_META','canvas.json')).write_text(json.dumps(meta,indent=0),encoding='utf-8');print('canvases',len(meta))


if __name__=='__main__':main()
