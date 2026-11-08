"""Read-only map tile extraction from actual native VRAM and ROM resources."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json,struct,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(PROJECT_ROOT))
from hd_core import Core,ROOT
from scripts.diagnostics.inspect_attract_resources import memory_chunk
import scripts.assets.srw_graphics as g
OUT=ROOT/'test_current/map_tiles';ASSET=ROOT/'graphics/map_tiles'

def decode_bg(core,mem,engine,layer):
    regs=mem['9REG'];base=0x1000 if engine else 0;cnt=int.from_bytes(regs[base+8+layer*2:base+10+layer*2],'little');disp=int.from_bytes(regs[base:base+4],'little')
    w,h=[(256,256),(512,256),(256,512),(512,512)][cnt>>14];addr=0x06200000 if engine else 0x06000000
    mapaddr=addr+((cnt>>8)&31)*2048+(0 if engine else ((disp>>27)&7)*65536)
    tileaddr=addr+((cnt>>2)&15)*16384+(0 if engine else ((disp>>24)&7)*65536)
    mb=C.create_string_buffer(w//8*h//8*2);tb=C.create_string_buffer(65536);core.api.retro_srw_copy_vram(mapaddr,mb,len(mb));core.api.retro_srw_copy_vram(tileaddr,tb,len(tb));palette=np.frombuffer(mem['VMEM'][1024:1536] if engine else mem['VMEM'][:512],'<u2');entries=np.frombuffer(mb.raw,'<u2');canvas=np.zeros((h,w,4),'uint8');eight=bool(cnt&128)
    for ty in range(h//8):
        for tx in range(w//8):
            entry=int(entries[((ty//32)*(w//256)+tx//32)*1024+(ty%32)*32+tx%32]);size=64 if eight else 32;raw=np.frombuffer(tb.raw[(entry&1023)*size:((entry&1023)+1)*size],'uint8');idx=raw.reshape(8,8) if eight else np.stack([raw&15,raw>>4],-1).reshape(8,8);colors=palette if eight else palette[(entry>>12)*16:((entry>>12)+1)*16];v=colors[idx].astype('uint32');rgba=np.stack([(v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31,(idx!=0)*255],-1).astype('uint8')
            if entry&1024:rgba=rgba[:,::-1]
            if entry&2048:rgba=rgba[::-1]
            canvas[ty*8:ty*8+8,tx*8:tx*8+8]=rgba
    return Image.fromarray(canvas),dict(engine=engine,layer=layer,cnt=cnt,disp=disp,mapaddr=mapaddr,tileaddr=tileaddr),tb.raw,mb.raw,palette

def main():
    OUT.mkdir(exist_ok=True);ASSET.mkdir(exist_ok=True);core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=OUT/'saves');core.load(ROOT/'test_current/font/menu_step_5.state');core.run();core.save(OUT/'capture.state');mem=memory_chunk(OUT/'capture.state');sheet=Image.new('RGB',(1024,512),'#444444');draw=ImageDraw.Draw(sheet);rows=[]
    try:
        for engine in range(2):
            for layer in range(4):
                image,info,tb,mb,pal=decode_bg(core,mem,engine,layer);image.save(OUT/f'engine_{engine}_layer_{layer}.png');np.savez_compressed(OUT/f'engine_{engine}_layer_{layer}.npz',tiles=np.frombuffer(tb,'uint8'),maps=np.frombuffer(mb,'uint8'),palette=pal);rows.append(info);copy=image.copy();copy.thumbnail((256,256));sheet.paste(copy,(layer*256,engine*256),copy);draw.text((layer*256,engine*256),f'{engine} {layer}',fill='red')
        sheet.save(OUT/'layers.png');Image.fromarray(core.native[192:]).save(OUT/'map_native.png');(OUT/'layers.json').write_text(json.dumps(rows,indent=2))
    finally:core.close()

if __name__=='__main__':main()
