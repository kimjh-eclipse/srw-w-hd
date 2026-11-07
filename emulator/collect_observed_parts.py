"""Collect visible battle hardware textures directly, without PAT UV guesses."""
import ctypes as C,json,zlib
import numpy as np
from hd_core import Core,ROOT
from audit_missing_parts import decode,SIZES
from inspect_attract_resources import snapshot

def main():
    out=ROOT/'test_current/attract';folder=out/'observed_parts';folder.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True,user_dir=out/'save_data')
    core.load(out/'target.state');records={};oam=C.create_string_buffer(1024);pal=C.create_string_buffer(512);regs=C.create_string_buffer(128);vram=C.create_string_buffer(131072)
    core.api.retro_srw_copy_obj_debug.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
    try:
        for f in range(8911,15001):
            core.run();core.audio.clear()
            if f in {13110,13350,13620,13920,14850}:snapshot(core,f);core.save(out/f'battle_{f}.state')
            if f%4:continue
            core.api.retro_srw_copy_obj_debug(oam,pal,regs);core.api.retro_srw_copy_vram(0x06400000,vram,131072);disp=int.from_bytes(regs.raw[:4],'little')
            for i,(a,b,c,_) in enumerate(np.frombuffer(oam.raw,'<u2').reshape(128,4)):
                a,b,c=map(int,(a,b,c));x=(b&511);y=a&255
                if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2:continue
                if x>=256:x-=512
                if y>=192:y-=256
                w,h=SIZES[a>>14][b>>14];extent=2 if a&256 and a&512 else 1
                if x>=256 or y>=120 or x+w*extent<=0 or y+h*extent<=0:continue
                key,ikey,idx,im,addr,colors=decode(vram.raw,pal.raw,a,b,c,disp)
                if not np.any(idx):continue
                if key not in records:
                    im.save(folder/f'{key:08x}.png');np.save(folder/f'{key:08x}.npy',idx)
                    rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).tolist()
                    records[key]=dict(hash=key,index_hash=ikey,w=w,h=h,first=f,last=f,count=0,palette_rgb=rgb)
                records[key]['last']=f;records[key]['count']+=1
            if f%600==0:print(f,len(records),flush=True)
    finally:core.close()
    (folder/'records.json').write_text(json.dumps(list(records.values()),indent=2));print('collected',len(records))

if __name__=='__main__':main()
