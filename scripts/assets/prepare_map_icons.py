"""Read-only map icon capture and archive-resource matching."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import ctypes as C,json,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from hd_core import Core,ROOT
from scripts.diagnostics.inspect_attract_resources import memory_chunk
from scripts.assets.audit_missing_parts import decode

def main():
    out=ROOT/'test_current/map_icons';out.mkdir(exist_ok=True);dest=ROOT/'graphics/map_icons';dest.mkdir(exist_ok=True)
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=out/'saves');records={}
    try:
        for state in ['map_fresh','menu_step_0','menu_step_1','menu_step_2','menu_step_3','menu_step_4','menu_step_5','grid']:
            core.load(ROOT/f'test_current/font/{state}.state');core.run();core.save(out/'capture.state');mem=memory_chunk(out/'capture.state')
            oam=np.frombuffer(mem['OAMS'][:1024],'<u2').reshape(128,4);pal=mem['VMEM'][512:1024];disp=int.from_bytes(mem['9REG'][:4],'little')
            vram=C.create_string_buffer(131072);core.api.retro_srw_copy_vram(0x06400000,vram,131072)
            Image.fromarray(core.native).save(out/(state+'_native.png'))
            for i,(a,b,c,_) in enumerate(oam):
                a,b,c=map(int,(a,b,c));x=b&511;y=a&255
                if x>=256:x-=512
                if y>=192:y-=256
                if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2:continue
                key,ikey,idx,im,address,colors=decode(vram.raw,pal,a,b,c,disp)
                if not idx.any() or x>=256 or y>=192 or x+im.width<=0 or y+im.height<=0:continue
                name=f'{key:08x}';im.save(dest/(name+'_native.png'));np.savez_compressed(dest/(name+'_native.npz'),indices=idx,palette=colors)
                entry=records.setdefault(name,dict(name=name,hash=key,index_hash=ikey,w=im.width,h=im.height,address=address,colors=colors.tolist(),observations=[]))
                entry['observations'].append(dict(state=state,oam=i,x=x,y=y,a=a,b=b,c=c))
    finally:core.close()
    rows=list(records.values());sheet=Image.new('RGB',(1024,((len(rows)+7)//8)*130),'#303030');d=ImageDraw.Draw(sheet)
    for j,r in enumerate(rows):
        im=Image.open(dest/(r['name']+'_native.png'));im.thumbnail((112,100));im=im.resize((im.width*min(4,112//im.width),im.height*min(4,112//im.width)),Image.Resampling.NEAREST);x=j%8*128;y=j//8*130;sheet.paste(im,(x,y),im);d.text((x,y+103),r['name'],fill='white');d.text((x,y+115),str((r['w'],r['h'])),fill='white')
    sheet.save(out/'native_contact.png');(dest/'observations.json').write_text(json.dumps(rows,indent=2));print('captured',len(rows))

if __name__=='__main__':main()
