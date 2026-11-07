"""Extract the full map-icon IMG block with its five affiliation palettes."""
import json,sys,hashlib
import numpy as np
from PIL import Image,ImageDraw
from hd_core import ROOT
sys.path.insert(0,str(ROOT))
from srw_graphics import archive,decompress,pixels,palette,BASE

def main():
    folder=ROOT/'graphics/map_icons';rom=(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds').read_bytes();offsets=archive(rom)
    raw=lambda i:decompress(rom[BASE+offsets[i]:BASE+offsets[i+1]])
    palettes={str(i):palette(raw(i)) for i in range(3938,3943)}; colors=np.array(palettes['3938'],dtype='uint8')
    records=[];unique={}
    for i in range(3944,4286):
        data=raw(i)
        if data[:3]!=b'IMG':continue
        idx=pixels(data)
        if idx.shape!=(16,16):continue
        key=hashlib.sha256(idx.tobytes()).hexdigest();record=dict(resource=i,duplicate_of=unique.get(key),sha256=key)
        if key not in unique:
            unique[key]=i;rgb=colors[idx].copy();rgb[:,:,3]=np.where(idx>0,255,0);Image.fromarray(rgb).save(folder/f'icon_{i}_native.png');np.save(folder/f'icon_{i}_indices.npy',idx)
        records.append(record)
    uniques=[r for r in records if r['duplicate_of'] is None];sheets=[]
    for batch in range((len(uniques)+31)//32):
        group=uniques[batch*32:(batch+1)*32];atlas=Image.new('RGBA',(1024,512))
        for j,r in enumerate(group):
            image=Image.open(folder/f"icon_{r['resource']}_native.png").resize((96,96),Image.Resampling.NEAREST);x=j%8*128+16;y=j//8*128+16;atlas.paste(image,(x,y));r.update(sheet=batch,cell=j)
        atlas.save(folder/f'sheet_{batch:02}_reference.png');sheets.append(dict(id=batch,resources=[r['resource'] for r in group],reference=f'sheet_{batch:02}_reference.png',generated=f'sheet_{batch:02}_hd.png',generated_ready=False))
    manifest=dict(source_range=[3944,4285],palettes=palettes,records=records,sheets=sheets,unique_icons=len(uniques),total_resources=len(records),complete=False)
    (folder/'library.json').write_text(json.dumps(manifest,indent=2));print('map icons',len(records),'unique',len(uniques),'sheets',len(sheets))

if __name__=='__main__':main()
