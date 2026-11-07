"""Decode every ROM MAP/CEL terrain set, retaining source identities."""
import sys,json,struct,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/map_tiles';TEST=ROOT/'test_current/map_tiles'

def main():
    OUT.mkdir(exist_ok=True);TEST.mkdir(exist_ok=True);rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    def raw(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    def kind(i):
        data=rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]];return data[16:20] if data[:4]==b'ECD\1' else data[:4]
    current={};rows=[];errors=[]
    for i in range(len(offsets)-1):
        tag=kind(i)
        if tag in (b'PLT\0',b'IMG\0',b'CEL\0'):current[tag]=i
        if tag!=b'MAP\0':continue
        try:
            mid=i;cid=current[b'CEL\0'];iid=current[b'IMG\0'];pid=current[b'PLT\0'];m=raw(mid);c=raw(cid);im=raw(iid);p=raw(pid)
            w,h=struct.unpack_from('<HH',m,4);w//=2;h//=2;mapidx=np.frombuffer(m[8:],'<u2').reshape(h,w);cells=np.frombuffer(c[8:],'<u2').reshape(-1,6);pixels=g.pixels(im);pal=np.array(g.palette(p),'uint8');tilew=pixels.shape[1]//8
            if int(mapidx.max())>=len(cells):raise ValueError('cell index out of bounds')
            atlas=Image.new('RGB',(256,((len(cells)+15)//16)*16));canvas=Image.new('RGB',(w*16,h*16));tileimgs=[]
            for j,cell in enumerate(cells):
                block=np.zeros((16,16,3),'uint8')
                for t,e in enumerate(cell[:4]):
                    e=int(e);tid=e&1023;tx=tid%tilew*8;ty=tid//tilew*8;idx=pixels[ty:ty+8,tx:tx+8];bank=e>>12
                    if idx.shape!=(8,8) or bank*16+int(idx.max())>=len(pal):raise ValueError('source tile or palette out of bounds')
                    colors=pal[bank*16:bank*16+16,:3][idx]
                    if e&1024:colors=colors[:,::-1]
                    if e&2048:colors=colors[::-1]
                    block[(t//2)*8:(t//2+1)*8,(t%2)*8:(t%2+1)*8]=colors
                image=Image.fromarray(block);tileimgs.append(image);atlas.paste(image,((j%16)*16,(j//16)*16))
            for y in range(h):
                for x in range(w):canvas.paste(tileimgs[int(mapidx[y,x])],(x*16,y*16))
            canvas.save(OUT/f'map_{mid}_native.png');atlas.save(OUT/f'cells_{cid}_native.png')
            np.savez_compressed(OUT/f'map_{mid}_layout.npz',indices=mapidx,cells=cells)
            rows.append(dict(id=mid,cel=cid,img=iid,pal=pid,native=f'map_{mid}_native.png',cells_image=f'cells_{cid}_native.png',cell_count=len(cells),width=w*16,height=h*16,status='native_extracted',source_sha256=hashlib.sha256(m+c+im+p).hexdigest()))
        except Exception as error:errors.append(dict(id=i,error=str(error),sources={k.hex():v for k,v in current.items()}))
    sheet=Image.new('RGB',(128*10,150*((len(rows)+9)//10)),'#222222');d=ImageDraw.Draw(sheet)
    for j,row in enumerate(rows):
        im=Image.open(OUT/row['native']);im.thumbnail((128,128));x=j%10*128;y=j//10*150;sheet.paste(im,(x,y));d.text((x,y+128),str(row['id']),fill='white')
    sheet.save(TEST/'all_maps_contact.png');manifest=dict(maps=rows,errors=errors,total_maps=len(rows)+len(errors),decoded_maps=len(rows),generated_maps=0,runtime_verified_maps=0)
    (OUT/'catalog.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(dict(total_maps=manifest['total_maps'],decoded_maps=len(rows),errors=errors)))

if __name__=='__main__':main()

