"""Extract registered full-screen scenario background tilemaps, read-only ROM."""
import json,hashlib,sys,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
import srw_graphics as g
ROOT=g.ROOT;OUT=ROOT/'graphics/scenario_backgrounds';TEST=ROOT/'test_current/scenario_backgrounds'

def decode(img,plt,scr):
    w,h=scr[5]*8,scr[6]*8;pal=np.asarray(g.palette(plt),dtype='uint8');idx=g.pixels(img);tiles=idx.reshape(idx.shape[0]//8,8,idx.shape[1]//8,8).transpose(0,2,1,3).reshape(-1,8,8)
    tiles=np.pad(tiles,((0,max(0,1024-len(tiles))),(0,0),(0,0)))
    entries=np.frombuffer(scr[8:],'<u2').reshape(h//8,w//8);canvas=np.zeros((h,w,4),dtype='uint8')
    for y in range(h//8):
        for x in range(w//8):
            entry=int(entries[y,x]);indices=tiles[entry&1023];bank=(entry>>12)*16
            if bank+int(indices.max())>=len(pal):raise ValueError('Palette bank out of range')
            pixels=pal[indices+bank].copy()
            if entry&1024:pixels=pixels[:,::-1]
            if entry&2048:pixels=pixels[::-1]
            canvas[y*8:y*8+8,x*8:x*8+8]=pixels
    return Image.fromarray(canvas)

def main():
    OUT.mkdir(exist_ok=True);TEST.mkdir(exist_ok=True)
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    def raw(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    records=[];sets=[(4780+i,4785+i,4790+i) for i in range(5)]+[(i,i+1,i+2) for i in range(4795,5523)]
    for p,i,s in sets:
        palette,img,scr=raw(p),raw(i),raw(s)
        if palette[:4]!=b'PLT\0' or img[:3]!=b'IMG' or scr[:4]!=b'SCR\0':continue
        image=decode(img,palette,scr);name=f'scenario_{s}';image.save(OUT/(name+'_native.png'));image.resize((image.width*4,image.height*4),Image.Resampling.NEAREST).save(OUT/(name+'_reference.png'))
        record=dict(name=name,palette=p,image_resource=i,map_resource=s,native=f'scenario_backgrounds/{name}_native.png',reference=f'scenario_backgrounds/{name}_reference.png',image=f'scenario_backgrounds/{name}_hd.png',native_size=list(image.size),source_tile_sha256=hashlib.sha256(img[8:]).hexdigest(),source_map_sha256=hashlib.sha256(scr[8:]).hexdigest(),source_tiles_crc32=zlib.crc32(img[8:]),source_map_crc32=zlib.crc32(scr[8:]),generated=(OUT/(name+'_hd.png')).exists(),registered=False,game_verified=False)
        records.append(record)
    for page in range((len(records)+23)//24):
        sheet=Image.new('RGB',(1024,624),'#222');d=ImageDraw.Draw(sheet)
        for n,row in enumerate(records[page*24:(page+1)*24]):
            x=n%6*170;y=n//6*156;im=Image.open(ROOT/'graphics'/row['native']).convert('RGB').resize((168,126));sheet.paste(im,(x,y));d.text((x,y+128),row['name'],fill='white')
        sheet.save(TEST/f'contact_{page}.png')
    (OUT/'catalog.json').write_text(json.dumps(dict(rom_sha256=hashlib.sha256(rom).hexdigest(),scope='Scenario map/CG/background PLT/IMG/SCR bank 4780-5523',resources=records,count=len(records),generated=sum(r['generated'] for r in records),registered=0,game_verified=0),indent=2));print('extracted',len(records))

if __name__=='__main__':main()
