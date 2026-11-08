"""Decode battle background layers from the ROM's exact 32-byte scene table."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json,hashlib,struct,zlib
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
ROOT=PROJECT_ROOT
sys.path.insert(0,str(ROOT));import scripts.assets.srw_graphics as g
F=ROOT/'graphics/battle_backgrounds';T=ROOT/'test_current/battle_backgrounds'

def decode(img,plt,scr):
    w,h=scr[5]*8,scr[6]*8;pal=np.asarray(g.palette(plt),dtype='uint8');idx=g.pixels(img)
    tiles=idx.reshape(idx.shape[0]//8,8,idx.shape[1]//8,8).transpose(0,2,1,3)
    # BG upload writes a rectangular IMG into 32-tile-wide VRAM rows.
    # Non-32-wide IMG assets otherwise decode into shuffled scenery.
    tiles=np.pad(tiles,((0,0),(0,max(0,32-tiles.shape[1])),(0,0),(0,0))).reshape(-1,8,8)
    tiles=np.pad(tiles,((0,max(0,1024-len(tiles))),(0,0),(0,0)))
    entries=np.frombuffer(scr[8:],'<u2').reshape(h//8,w//8);canvas=np.zeros((h,w,4),dtype='uint8');materials=np.zeros((h,w),dtype='uint8')
    for y in range(h//8):
        for x in range(w//8):
            entry=int(entries[y,x]);indices=tiles[entry&1023];bank=(entry>>12)*16
            colors=pal[indices+bank].copy();colors[:,:,3]=np.where(indices==0,0,255)
            material=(indices+bank).astype('uint8');material=np.where(indices==0,0,material).astype('uint8')
            if entry&1024:colors=colors[:,::-1];material=material[:,::-1]
            if entry&2048:colors=colors[::-1];material=material[::-1]
            canvas[y*8:y*8+8,x*8:x*8+8]=colors
            materials[y*8:y*8+8,x*8:x*8+8]=material
    return Image.fromarray(canvas),materials

def main():
    F.mkdir(exist_ok=True);T.mkdir(exist_ok=True)
    rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=g.archive(rom)
    cache={}
    def raw(i):
        if i not in cache:cache[i]=g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
        return cache[i]
    scenes=[];keys={}
    for at in range(0x163ecc,0x16598d,32):
        values=struct.unpack_from('<16H',rom,at)
        if not 6446<=values[0]<=6871 or raw(values[0])[:3]!=b'PLT':continue
        if not all(values[s]==65535 or(raw(values[s])[:3]==b'IMG' and raw(values[s+1])[:3]==b'SCR') for s in [4,10]):continue
        scene=dict(address=hex(at),table_index=(at-0x163ecc)//32,palette=values[0],layers=[])
        for layer,s in [(2,4),(3,10)]:
            if values[s]==65535:continue
            key=(values[0],values[s],values[s+1]);scene['layers'].append(dict(layer=layer,key=list(key)))
            keys.setdefault(key,[]).append(dict(scene=scene['table_index'],layer=layer))
        scenes.append(scene)
    rows=[];pixelhashes={}
    for (p,i,s),uses in sorted(keys.items()):
        image,materials=decode(raw(i),raw(p),raw(s));digest=hashlib.sha256(image.tobytes()).hexdigest();name=f'battle_{p}_{i}_{s}'
        image.save(F/f'{name}_native.png')
        Image.fromarray(materials).save(F/f'{name}_indices.png')
        # Composite transparent tile index zero over black for source-atlas drawing.
        reference=Image.new('RGB',image.size,'black');reference.paste(image,mask=image.getchannel('A'));reference.save(F/f'{name}_reference.png')
        owner=pixelhashes.setdefault(digest,name)
        rows.append(dict(name=name,palette=p,image_resource=i,map_resource=s,native=f'battle_backgrounds/{name}_native.png',reference=f'battle_backgrounds/{name}_reference.png',image=f'battle_backgrounds/{owner}_hd.png',indices=f'battle_backgrounds/{name}_indices.png',geometry_sha256=hashlib.sha256(struct.pack('<HH',*image.size)+materials.tobytes()).hexdigest(),palette_rgb=[list(c[:3]) for c in g.palette(raw(p))],native_size=list(image.size),native_pixel_sha256=digest,art_owner=owner,source_tiles_crc32=zlib.crc32(raw(i)[8:]),source_map_crc32=zlib.crc32(raw(s)[8:]),uses=uses,generated=(F/f'{owner}_hd.png').exists(),registered=False,game_verified=False))
    meta=dict(scope='Exact battle background descriptor table 0x163ECC..0x16598C, excluding zero entries',scenes=scenes,scene_count=len(scenes),unique_resource_combinations=len(rows),unique_pixel_images=len(pixelhashes),resources=rows)
    (F/'catalog.json').write_text(json.dumps(meta,indent=2))
    unique=[r for r in rows if r['name']==r['art_owner']]
    for page in range((len(unique)+23)//24):
        sheet=Image.new('RGB',(1024,624),'#222');d=ImageDraw.Draw(sheet)
        for n,row in enumerate(unique[page*24:(page+1)*24]):
            x=n%6*170;y=n//6*156;im=Image.open(ROOT/'graphics'/row['reference']);im.thumbnail((168,126));sheet.paste(im,(x,y));d.text((x,y+128),str(page*24+n)+':'+str(row['map_resource']),fill='white')
        sheet.save(T/f'contact_{page}.png')
    print(json.dumps({k:v for k,v in meta.items() if k not in ['resources','scenes']}))

if __name__=='__main__':main()
