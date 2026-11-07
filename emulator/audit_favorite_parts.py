import ctypes as C,json
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from frame_compositor import ReadyParts
from inspect_attract_resources import memory_chunk
from audit_missing_parts import decode
from tile_compositor import TileCompositor

def main():
    out=ROOT/'test_current/formation';core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'boot_saves');core.set_ready_parts(ReadyParts());core.load(out/'formation.state');core.run();core.save(out/'inspect.state');mem=memory_chunk(out/'inspect.state');vram=C.create_string_buffer(131072);core.api.retro_srw_copy_vram(0x06600000,vram,131072);a=np.frombuffer(core.obj.raw,'<u2').reshape(128,4);disp=int.from_bytes(mem['9REG'][4096:4100],'little');pal=mem['VMEM'][1536:2048];tiles=TileCompositor();rows=[];canvas=Image.new('RGB',(1024,768),'#444444');d=ImageDraw.Draw(canvas)
    try:
        for i,(aa,b,c,_) in enumerate(a):
            aa,b,c=map(int,(aa,b,c))
            if (not aa&256 and aa&512) or aa>>14==3:continue
            key,ikey,idx,im,address,colors=decode(vram.raw,pal,aa,b,c,disp)
            if not idx.any():continue
            blocks=[idx[y:y+8,x:x+8] for y in range(0,idx.shape[0],8) for x in range(0,idx.shape[1],8) if idx[y:y+8,x:x+8].any()];found=sum(bool(tiles.find(t.tobytes())) for t in blocks)
            np.savez_compressed(out/f'part_{i}.npz',indices=idx,palette=colors);im.save(out/f'part_{i}.png');row=dict(oam=i,w=im.width,h=im.height,a=aa,b=b,c=c,hash=key,index_hash=ikey,binding=int(core.parts[i,0]),tiles=len(blocks),matched_tiles=found);rows.append(row);x=(len(rows)-1)%8*128;y=(len(rows)-1)//8*128;im=im.resize((im.width*2,im.height*2),Image.Resampling.NEAREST);canvas.paste(im,(x,y),im);d.text((x,y+112),f'{i}: {found}/{len(blocks)}',fill='yellow')
        canvas.save(out/'parts_contact.png');(out/'parts_audit.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows))
    finally:core.close();tiles.db.close()

if __name__=='__main__':main()
