"""Extract every chapter title's real IMG/SCR composition from the ROM."""
import sys,json,hashlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/localized_screens';TEST=ROOT/'test_current/localized_screens'

def main():
    OUT.mkdir(exist_ok=True);TEST.mkdir(exist_ok=True);rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();o=g.archive(rom)
    def raw(i):return g.decompress(rom[g.BASE+o[i]:g.BASE+o[i+1]])
    palette=np.array(g.palette(raw(5928)),'uint8');rows=[];sheets=[Image.new('RGB',(512*4,140*9),'#111111') for _ in range(2)]
    for n in range(70):
        iid=5930+n;sid=6000+n;img=raw(iid);scr=raw(sid);assert img[:3]==b'IMG' and scr[:3]==b'SCR';pixels=g.pixels(img);entries=np.frombuffer(scr[8:],'<u2').reshape(24,32);canvas=np.zeros((192,256,4),'uint8');indices=np.zeros((192,256),'uint8')
        for ty in range(24):
            for tx in range(32):
                e=int(entries[ty,tx]);tid=e&1023;idx=pixels[tid//32*8:tid//32*8+8,tid%32*8:tid%32*8+8];colors=palette[idx].copy();colors[:,:,3]=(idx!=0)*255
                if e&1024:colors=colors[:,::-1];idx=idx[:,::-1]
                if e&2048:colors=colors[::-1];idx=idx[::-1]
                canvas[ty*8:ty*8+8,tx*8:tx*8+8]=colors;indices[ty*8:ty*8+8,tx*8:tx*8+8]=idx
        image=Image.fromarray(canvas);image.save(OUT/f'chapter_{n:02}_native.png');ink=np.all(canvas[:,:,:3]>210,axis=2)&(canvas[:,:,3]>0);np.savez_compressed(OUT/f'chapter_{n:02}_mask.npz',ink=ink)
        row=dict(index=n,img=iid,scr=sid,native=f'chapter_{n:02}_native.png',status='native_extracted',ink_sha256=hashlib.sha256(np.packbits(ink).tobytes()).hexdigest(),source_sha256=hashlib.sha256(img+scr).hexdigest());rows.append(row)
        contact=image.crop((0,48,256,118)).resize((512,140),Image.Resampling.NEAREST);j=n%35;x=j%4*512;y=j//4*140;sheets[n//35].paste(contact,(x,y),contact);ImageDraw.Draw(sheets[n//35]).text((x,y),str(n),fill='red')
    for i,sheet in enumerate(sheets):sheet.save(TEST/f'chapter_titles_{i}.png')
    (OUT/'chapter_catalog.json').write_text(json.dumps(dict(titles=rows,total_titles=70,translated_titles=0),indent=2));print('Extracted',len(rows),'chapter titles')

if __name__=='__main__':main()
