"""Connect the title logo master (test_current/parts/title_logo_hd) as OBJ parts.

The logo is drawn as sprites (PAT39 over IMG38). The live title state gives
every logo sprite the core has no HD art for (unknown parts: index hash, OAM
attributes, RGB hash, cached indices and palette). Each sprite's HD picture
is cut from the 4x master at its screen place (logo box origin = screen
4,48), un-flipped to the cached texture orientation, packed into a sheet with
its native reference, and installed as new parts.
"""
import base64,hashlib,json,sys,zlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]));sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'emulator'))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image

STATE='test_current/ui/start_menu_source/start180.state'
SRC=ROOT/'test_current/parts/title_logo_hd';OUT=SRC/'claude_obj_package'
BOX=(4,48,252,152)


def main():
    from hd_core import Core
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=OUT/'saves')
    core.load(ROOT/STATE)
    for _ in range(3):core.run();core.audio.clear()
    snap=core.unknown_snapshot();core.close()
    assert snap is not None,'no unknown OBJ'
    rows,pixels,palettes=snap
    master=Image.open(SRC/'candidate_logo.png').convert('RGBA')
    pieces=[];seen=set()
    for i in range(128):
        r=rows[i]
        if not r[0]:continue
        ih,w,h,a,b,c,hsh,mat=map(int,r)
        if a&256:continue                       # affine: not handled here
        x=b&511;y=a&255
        if x>=256:x-=512
        if y>=192:y-=256
        if x+w<=BOX[0] or x>=BOX[2] or y+h<=BOX[1] or y>=BOX[3]:continue
        if hsh in seen:continue
        idx=pixels[i][:w*h].reshape(h,w).copy();pal=palettes[i].astype('uint32')
        hx,hy=bool(b&0x1000),bool(b&0x2000)
        art=master.crop(((x-BOX[0])*4,(y-BOX[1])*4,(x-BOX[0]+w)*4,(y-BOX[1]+h)*4))
        if hx:art=art.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if hy:art=art.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        if np.asarray(art)[:,:,3].max()<16:continue
        seen.add(hsh);pieces.append((idx,pal,art,ih,hsh,w,h,x,y))
    assert pieces,'no logo sprites found'
    # Pack into a sheet, 8-px aligned rows.
    width=256;cx=cy=rowh=0;placed=[]
    for p in sorted(pieces,key=lambda p:-p[6]):
        w,h=p[5],p[6]
        if cx+w>width:cx=0;cy+=rowh;rowh=0
        placed.append((p,cx,cy));cx+=w;rowh=max(rowh,h)
    H=cy+rowh;native=np.zeros((H,width,4),dtype='uint8');hd=Image.new('RGBA',(width*4,H*4));contract=[]
    for (idx,pal,art,ih,hsh,w,h,x,y),ax,ay in placed:
        rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1).astype('uint8')
        native[ay:ay+h,ax:ax+w,:3]=rgb[idx];native[ay:ay+h,ax:ax+w,3]=np.where(idx>0,255,0)
        hd.alpha_composite(art,(ax*4,ay*4))
        mask=idx>0
        assert (zlib.crc32(np.where(mask,idx.astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h)==ih
        assert (zlib.crc32(np.where(mask,pal[idx].astype('uint16')|0x8000,0).astype('<u2').tobytes())^(w<<16)^h)==hsh
        contract.append(dict(slot=len(contract),hash=hsh,index_hash=ih,atlas_box=[ax,ay,w,h],index_pixels=base64.b64encode(zlib.compress(idx.astype('uint8').tobytes())).decode(),
            actual_palette_bgr555=[int(v) for v in pal],actual_palette_rgb=[[int(v) for v in c] for c in rgb],resource=38,source_x=x,source_y=y,w=w,h=h,
            render_mode='static',effect_part=False,actual_observed=True,source_owner=38,note='title logo sprite; screen position recorded as source_x/y'))
    OUT.mkdir(parents=True,exist_ok=True)
    Image.fromarray(native).save(OUT/'native.png');hd.save(OUT/'candidate.png');master.save(OUT/'generated.png')
    (OUT/'contract.json').write_text(json.dumps(contract,ensure_ascii=False),encoding='utf-8')
    sha=lambda f:hashlib.sha256((OUT/f).read_bytes()).hexdigest()
    entry=dict(source=str(OUT.relative_to(ROOT)).replace('\\','/'),contract='contract.json',drawing='candidate.png',native='native.png',generated='generated.png',bindings=[],
        new_source_keys=[dict(hash=r['hash'],index_hash=r['index_hash']) for r in contract],file_sha256=dict(contract=sha('contract.json'),drawing=sha('candidate.png'),native=sha('native.png'),generated=sha('generated.png')))
    (OUT/'entry.json').write_text(json.dumps(entry,ensure_ascii=False,indent=1),encoding='utf-8')
    print('logo sprites',len(contract),'sheet',width,H)


if __name__=='__main__':main()
