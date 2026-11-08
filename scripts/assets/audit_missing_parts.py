"""Collect visible native OBJ textures not yet covered by the HD library."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json,zlib,re,hashlib
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT,HERE

SIZES=[[(8,8),(16,16),(32,32),(64,64)],[(16,8),(32,8),(32,16),(64,32)],[(8,16),(8,32),(16,32),(32,64)]]
def decode(vram,palette,a,b,c,disp):
    w,h=SIZES[a>>14][b>>14];eight=bool(a&8192);tile_bytes=64 if eight else 32;one=bool(disp&16)
    address=(c&1023)<<(5+((disp>>20)&3) if one else 5);stride=w//8*tile_bytes if one else 1024
    blocks=[np.frombuffer(vram[address+ty*stride+tx*tile_bytes:address+ty*stride+tx*tile_bytes+tile_bytes],dtype='uint8') for ty in range(h//8) for tx in range(w//8)]
    raw=np.concatenate(blocks)
    if not eight:raw=np.stack([raw&15,raw>>4],-1).reshape(-1)
    idx=raw.reshape(h//8,w//8,8,8).transpose(0,2,1,3).reshape(h,w)
    colors=np.frombuffer(palette,'<u2')[0:256] if eight else np.frombuffer(palette,'<u2')[(c>>12)*16:((c>>12)+1)*16]
    encoded=np.where(idx!=0,colors[idx]|0x8000,0).astype('<u2');key=zlib.crc32(encoded.tobytes())^(w<<16)^h
    indexed=np.where(idx!=0,idx.astype('uint16')|0x8000,0).astype('<u2');index_key=zlib.crc32(indexed.tobytes())^(w<<16)^h
    rgb=np.stack([(encoded&31)*255//31,((encoded>>5)&31)*255//31,((encoded>>10)&31)*255//31],-1).astype('uint8')
    return key,index_key,idx,Image.fromarray(np.dstack([rgb,(idx!=0).astype('uint8')*255])),address,colors

def main():
    out=ROOT/'test_current/parts';out.mkdir(exist_ok=True)
    library=json.loads((ROOT/'graphics/kazuma_parts_library.json').read_text());known={p['hash'] for p in library['bindings'] if p.get('rgb_enabled',True) and not p.get('disabled')};records={}
    known_index={p['index_hash'] for p in library['bindings'] if p.get('dynamic_palette') and p.get('indexed_safe',True) and not p.get('disabled')} - set(library.get('indexed_collision_keys',[]))
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=False,demo=True);core.load(HERE/'demo.state',refresh_code=True)
    events=json.loads((HERE/'demo_input.json').read_text());oam=C.create_string_buffer(1024);pal=C.create_string_buffer(512);regs=C.create_string_buffer(128);vram=C.create_string_buffer(131072)
    for f in range(64700,67101):
        core.buttons={e['button'] for e in events if e['from']<=f<e['to']};core.run();core.audio.clear()
        if f<64960:continue
        core.api.retro_srw_copy_obj_debug(oam,pal,regs);core.api.retro_srw_copy_vram(0x06400000,vram,131072);disp=int.from_bytes(regs.raw[:4],'little')
        raw_oam=np.frombuffer(oam.raw,'<u2').reshape(128,4)
        for i,(a,b,c,_) in enumerate(raw_oam):
            a,b,c=map(int,(a,b,c));x=b&511;y=a&255
            if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2:continue
            w,h=SIZES[a>>14][b>>14];extent=2 if a&256 and a&512 else 1
            if x>=256:x-=512
            if y>=192:y-=256
            if x>=256 or y>=192 or x+w*extent<=0 or y+h*extent<=0:continue
            key,index_key,idx,im,address,colors=decode(vram.raw,pal.raw,a,b,c,disp)
            if key in known or index_key in known_index or not np.any(idx):continue
            if key not in records:
                im.save(out/f'missing_{key:08x}.png')
                records[key]=dict(hash=key,index_hash=index_key,first=f,last=f,count=0,w=im.width,h=im.height,address=address,palette=c>>12,palette_colors=[int(v) for v in colors],oam=i)
            records[key]['count']+=1;records[key]['last']=f
    core.close();items=sorted(records.values(),key=lambda r:(r['first'],r['address']))
    (out/'missing_parts.json').write_text(json.dumps(items,indent=2))
    cells=[r for r in items if r['count']>=2];sheet=Image.new('RGB',(1200,((len(cells)+7)//8)*130),(28,32,40));d=ImageDraw.Draw(sheet)
    for j,r in enumerate(cells):
        im=Image.open(out/f"missing_{r['hash']:08x}.png");scale=min(3,130/im.width,85/im.height);im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.NEAREST);x=j%8*150;y=j//8*130
        sheet.paste(im,(x+8,y+32),im);d.text((x+5,y+3),f"{j}: p{r['palette']} {r['count']}x",fill='white');d.text((x+5,y+17),f"{r['first']} {r['address']:04x}",fill='white')
    sheet.save(out/'missing_parts_sheet.png')
    # Only obsolete images produced by this audit are removed. Keep the fixed
    # report path and unrelated graphics/tests intact.
    keep={f'missing_{r["hash"]:08x}.png' for r in items}
    for path in out.glob('missing_????????.png'):
        if re.fullmatch(r'missing_[0-9a-f]{8}\.png',path.name) and path.name not in keep:path.unlink()
    report=dict(unique_missing=len(items),repeated=len(cells),by_palette=dict(Counter(r['palette'] for r in items)),frames=[64960,67100],library_sha256=hashlib.sha256((ROOT/'graphics/kazuma_parts_library.json').read_bytes()).hexdigest(),full_game_verified=False)
    (out/'missing_parts_scope.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

if __name__=='__main__':main()
