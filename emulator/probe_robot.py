"""Inspect live battle OBJ resources without changing game data."""
import ctypes as C,json,struct
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT,HERE

SIZES=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]]
def snapshot(core,out,frame):
    oam=C.create_string_buffer(1024);pal=C.create_string_buffer(512);regs=C.create_string_buffer(128);vram=C.create_string_buffer(0x20000)
    core.api.retro_srw_copy_obj_debug(oam,pal,regs);core.api.retro_srw_copy_vram(0x06400000,vram,0x20000)
    disp=struct.unpack_from('<I',regs.raw)[0];boundary=5+((disp>>20)&3)
    colors=np.frombuffer(pal.raw,'<u2').astype('uint32');rgb=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],-1).astype('uint8')
    sheet=Image.new('RGBA',(1024,1024),(30,30,30,255));d=ImageDraw.Draw(sheet);entries=[]
    for i in range(128):
        a,b,c,_=struct.unpack_from('<4H',oam.raw,i*8)
        if not a&256 and a&512:continue
        shape=a>>14
        if shape==3:continue
        w,h=SIZES[shape][b>>14];x=b&511;x=x if x<256 else x-512;y=a&255;y=y if y<192 else y-256
        addr=(c&1023)<<boundary;bits=8 if a&8192 else 4
        raw=(np.frombuffer(vram.raw[addr:addr+w*h*bits//8],dtype='uint8') if disp&16 else np.concatenate([np.frombuffer(vram.raw[addr+ty*1024+tx*(64 if bits==8 else 32):addr+ty*1024+tx*(64 if bits==8 else 32)+(64 if bits==8 else 32)],dtype='uint8') for ty in range(h//8) for tx in range(w//8)]))
        if len(raw)<w*h*bits//8:continue
        if bits==4:raw=np.stack([raw&15,raw>>4],-1).reshape(-1)
        idx=raw.reshape(h//8,w//8,8,8).transpose(0,2,1,3).reshape(h,w)
        pix=rgb[idx+(0 if bits==8 else (c>>12)*16)];alpha=(idx!=0).astype('uint8')*255
        im=Image.fromarray(np.dstack([pix,alpha]))
        if not a&256:
            if b&4096:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if b&8192:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        im.save(out/f'obj_{frame}_{i}.png')
        sx=(i%16)*64;sy=(i//16)*128;sheet.paste(im,(sx,sy+20),im);d.text((sx,sy),f'{i}: {x},{y}',fill='white')
        entries.append(dict(i=i,a=a,b=b,c=c,x=x,y=y,w=w,h=h,addr=addr,affine=bool(a&256),matrix=(b>>9)&31,prio=(c>>10)&3))
    assembled=Image.new('RGBA',(256,192))
    for e in reversed(entries):
        if e['c']>>12==0:
            im=Image.open(out/f"obj_{frame}_{e['i']}.png");assembled.alpha_composite(im,(e['x'],e['y']))
    assembled.save(out/f'robot_{frame}.png')
    sheet.save(out/f'obj_sheet_{frame}.png');(out/f'obj_{frame}.json').write_text(json.dumps(dict(dispcnt=hex(disp),boundary=boundary,entries=entries),indent=2))
    (out/f'oam_{frame}.bin').write_bytes(oam.raw);(out/f'vram_{frame}.bin').write_bytes(vram.raw);(out/f'pal_{frame}.bin').write_bytes(pal.raw)
    Image.fromarray(core.native).save(out/f'native_{frame}.png')

if __name__=='__main__':
    out=ROOT/'test_current/robot';out.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True);core.load(HERE/'demo.state',refresh_code=True)
    events=json.loads((HERE/'demo_input.json').read_text())
    for f in range(64700,66001):
        core.buttons={e['button'] for e in events if e['from']<=f<e['to']};core.run();core.audio.clear()
        if f in [65040,65160,65220,65280,65340,65400,65520,65700,66000]:snapshot(core,out,f)
    core.close()
