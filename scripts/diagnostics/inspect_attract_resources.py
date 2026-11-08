"""Extract exact native battle OBJ/BG textures and palette state, read-only."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json,struct,zlib
import numpy as np
from PIL import Image
from hd_core import Core,ROOT
from scripts.assets.audit_missing_parts import decode
OUT=ROOT/'test_current/attract'
def memory_chunk(path):
    raw=path.read_bytes();data=raw[32:] if struct.unpack_from('<I',raw,28)[0]==0xffffffff else zlib.decompress(raw[32:])
    at=0
    while at+8<=len(data):
        kind,size=struct.unpack_from('<II',data,at);at+=8
        if kind==4:
            stop=at+size;result={}
            while at<stop:
                tag=data[at:at+4].decode('ascii');width,count=struct.unpack_from('<II',data,at+4);at+=12
                result[tag]=data[at:at+width*count];at+=width*count
            return result
        at+=size
    raise ValueError('Memory chunk missing')
def snapshot(core,frame):
    core.save(OUT/'capture.state');memory=memory_chunk(OUT/'capture.state');pal=memory['VMEM'];vram=C.create_string_buffer(131072)
    oam=memory['OAMS'][:1024];regs=memory['9REG'][:128];disp=int.from_bytes(regs[:4],'little')
    core.api.retro_srw_copy_vram(0x06400000,vram,131072)
    obj=[]
    for i,(a,b,c,_) in enumerate(np.frombuffer(oam,'<u2').reshape(128,4)):
        a,b,c=map(int,(a,b,c))
        if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2:continue
        key,ikey,idx,im,address,colors=decode(vram.raw,pal[512:1024],a,b,c,disp)
        if not np.any(idx):continue
        im.save(OUT/f'obj_{frame}_{i:03}.png');obj.append(dict(oam=i,hash=key,index_hash=ikey,x=(b&511) if b&511<256 else (b&511)-512,y=(a&255) if a&255<192 else (a&255)-256,w=im.width,h=im.height,a=a,b=b,c=c,palette_colors=[int(v) for v in colors],address=address))
    np.savez_compressed(OUT/f'obj_{frame}.npz',oam=np.frombuffer(oam,'uint8'),palette=np.frombuffer(pal,'uint8'),regs=np.frombuffer(regs,'uint8'),vram=np.frombuffer(vram.raw,'uint8'))
    (OUT/f'obj_{frame}.json').write_text(json.dumps(obj,indent=2))
    layers=[]
    for layer in range(4):
        info=(C.c_uint*9)();core.api.retro_srw_get_bg_info(layer,info);cnt,map_addr,tiles,x,y,w,h,visible,prio=map(int,info)
        if not visible or w not in (256,512) or h not in (256,512):continue
        maps=C.create_string_buffer(w//8*h//8*2);tiles_raw=C.create_string_buffer(65536)
        core.api.retro_srw_copy_vram(map_addr,maps,len(maps));core.api.retro_srw_copy_vram(tiles,tiles_raw,65536)
        palette=np.frombuffer(pal[1024:1536] if map_addr>=0x06200000 else pal[:512],'<u2')
        canvas=np.zeros((h,w,4),dtype='uint8');entries=np.frombuffer(maps.raw,'<u2');eight=bool(cnt&128)
        for ty in range(h//8):
            for tx in range(w//8):
                entry=int(entries[((ty//32)*(w//256)+tx//32)*1024+(ty%32)*32+tx%32]);tile=entry&1023
                raw=np.frombuffer(tiles_raw.raw[tile*(64 if eight else 32):(tile+1)*(64 if eight else 32)],'uint8')
                idx=raw.reshape(8,8) if eight else np.stack([raw&15,raw>>4],-1).reshape(8,8)
                colors=palette if eight else palette[(entry>>12)*16:((entry>>12)+1)*16];v=colors[idx].astype('uint32')
                rgba=np.stack([(v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31,(idx!=0)*255],-1).astype('uint8')
                if entry&1024:rgba=rgba[:,::-1]
                if entry&2048:rgba=rgba[::-1]
                canvas[ty*8:ty*8+8,tx*8:tx*8+8]=rgba
        Image.fromarray(canvas).save(OUT/f'bg_{frame}_{layer}.png')
        np.savez_compressed(OUT/f'bg_{frame}_{layer}.npz',info=np.array(info),map=np.frombuffer(maps.raw,'uint8'),tiles=np.frombuffer(tiles_raw.raw,'uint8'),palette=palette)
        layers.append(dict(layer=layer,info=list(info)))
    (OUT/f'bg_{frame}.json').write_text(json.dumps(layers,indent=2));Image.fromarray(core.native[:192]).save(OUT/f'native_{frame}.png')
def main():
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=OUT/'save_data')
    wanted={5910,6030,6120,6900,7040,7080,8100,8130,8800,8910,9900,10100}
    try:
        for f in range(max(wanted)+1):
            core.run();core.audio.clear()
            if f in wanted:snapshot(core,f);print('captured',f,flush=True)
    finally:core.close()
if __name__=='__main__':main()
