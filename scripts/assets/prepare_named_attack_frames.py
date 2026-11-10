"""Extract omitted attack IMG frames using palettes actually observed in battle."""
import json,sys,zlib
from pathlib import Path
from collections import Counter,defaultdict
import numpy as np
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g

def main():
    resources=[8264,8265,8287,15026,11079,11202,8805,8812,8826,8832,18170,10780,7152,17168,1775,7656]
    report=json.loads((ROOT/'test_current/parts/observed_attack_gaps/report.json').read_text())
    matches=report['rom_tile_matches'];wanted=set(resources);votes=defaultdict(Counter);palettes={}
    for path in sorted((ROOT/'test_current/combat/named_attacks').glob('unit_*/*_unknown.npz')):
        with np.load(path) as data:
            for row,raw,pal in zip(data['rows'],data['pixels'],data['palettes']):
                w,h=map(int,row[1:3]);a=raw[:w*h].reshape(h,w);key=pal.tobytes();palettes[key]=pal.copy()
                for y in range(0,h,8):
                    for x in range(0,w,8):
                        tile=a[y:y+8,x:x+8]
                        if not tile.any():continue
                        for resource in set(matches.get(str(zlib.crc32(tile.tobytes())),[]))&wanted:
                            votes[resource][key]+=int(np.count_nonzero(tile))
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    folder=ROOT/'graphics/named_attack_frames';folder.mkdir(exist_ok=True);sheets=[]
    for page in range(4):
        canvas=Image.new('RGBA',(256,320));items=[]
        for slot,resource in enumerate(resources[page*4:page*4+4]):
            assert votes[resource],('No live palette',resource)
            key,score=votes[resource].most_common(1)[0];pal=palettes[key].astype('uint32')
            rgb=np.stack([(pal&31)*255//31,((pal>>5)&31)*255//31,((pal>>10)&31)*255//31],-1).astype('uint8')
            a=g.pixels(g.decompress(rom[g.BASE+offsets[resource]:g.BASE+offsets[resource+1]]));h,w=a.shape
            assert w<=256 and h<=80
            rgba=np.dstack([rgb[a],(a!=0).astype('uint8')*255]);rgba[a==0]=0
            native=Image.fromarray(rgba);native.save(folder/f'frame_{resource}_native.png');canvas.paste(native,(0,slot*80))
            items.append(dict(resource=resource,slot=slot,x=0,y=slot*80,w=w,h=h,palette_rgb=rgb.tolist(),observed_palette_votes=score))
        name=f'attack_{page:02}';canvas.save(folder/f'{name}_native.png');canvas.resize((768,960),Image.Resampling.NEAREST).save(folder/f'{name}_reference.png')
        sheets.append(dict(name=name,output=f'{name}_generated.png',native_size=[256,320],items=items))
    (folder/'plan.json').write_text(json.dumps(dict(scope=__doc__,sheets=sheets),indent=2))
    print('Extracted',len(resources),'native resources with observed palettes')

if __name__=='__main__':main()
