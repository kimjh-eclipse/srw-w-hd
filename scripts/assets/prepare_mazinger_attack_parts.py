"""Extract compact source banks for the reported FDS robots, using live OBJ palettes."""
import json,sys,zlib
from pathlib import Path
from collections import Counter
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
from scripts.assets.audit_missing_parts import decode

def main():
    resources=(2613,2645,2654,14462,14510,14882,14886,14887)
    folder=ROOT/'graphics/mazinger_attack_parts';folder.mkdir(exist_ok=True)
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    arrays={i:g.pixels(g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])) for i in resources}
    wanted={i:{a[y:y+8,x:x+8].tobytes() for y in range(0,a.shape[0],8) for x in range(0,a.shape[1],8) if len(np.unique(a[y:y+8,x:x+8]))>=3} for i,a in arrays.items()}
    votes={i:Counter() for i in resources};palettes={}
    paths=list((ROOT/'test_current/combat/mazinger_combination').glob('obj_*.npz'))
    paths+=list((ROOT/'test_current/combat/named_attacks/unit_297/diagnostic_preview/weapon_1213_capture').glob('obj_*.npz'))
    for path in paths:
        with np.load(path) as d:
            vram=d['vram'].tobytes();palette=d['palette'].tobytes()[512:1024];disp=int.from_bytes(d['regs'].tobytes()[:4],'little')
            for a,b,c,_ in np.frombuffer(d['oam'].tobytes(),'<u2').reshape(128,4):
                a,b,c=map(int,(a,b,c))
                if (not a&256 and a&512) or a>>14==3 or (a>>10)&3>=2 or a&8192:continue
                _,_,indices,_,_,colors=decode(vram,palette,a,b,c,disp)
                if not indices.any():continue
                key=colors.tobytes();palettes[key]=colors.copy()
                for y in range(0,indices.shape[0],8):
                    for x in range(0,indices.shape[1],8):
                        tile=indices[y:y+8,x:x+8];blob=tile.tobytes()
                        for resource in resources:
                            if blob in wanted[resource]:votes[resource][key]+=int(np.count_nonzero(tile))
    items=[];cards=[]
    # One IMG can contain pieces from all three robots. Palette is attached
    # to each live OBJ rectangle, not to the entire IMG bank.
    cell_votes={i:{} for i in resources};offset_cache={}
    for path in (ROOT/'test_current/combat/mazinger_combination').glob('parts_*.json'):
        frame=path.stem.split('_')[1];npz=path.with_name(f'obj_{frame}.npz')
        metadata=json.loads(path.read_text())
        with np.load(npz) as d:
            vram=d['vram'].tobytes();palette=d['palette'].tobytes()[512:1024];disp=int.from_bytes(d['regs'].tobytes()[:4],'little')
            for i,(aa,bb,cc,_) in enumerate(np.frombuffer(d['oam'].tobytes(),'<u2').reshape(128,4)):
                binding=metadata['parts'][i][0]
                if not binding:continue
                spec=metadata['bindings'][str(binding)];resource=spec.get('resource')
                if resource not in arrays:continue
                _,index_hash,indices,_,_,colors=decode(vram,palette,int(aa),int(bb),int(cc),disp)
                h,w=indices.shape;key=(resource,index_hash,w,h);palkey=colors.tobytes();palettes[palkey]=colors.copy()
                if key not in offset_cache:
                    source=arrays[resource];padded=np.pad(source,((0,64),(0,64)));found=[]
                    for sy in range(0,source.shape[0],8):
                        for sx in range(0,source.shape[1],8):
                            if np.array_equal(padded[sy:sy+h,sx:sx+w],indices):found.append((sx,sy))
                    offset_cache[key]=found
                for sx,sy in offset_cache[key]:
                    for y in range(0,h,8):
                        for x in range(0,w,8):
                            if sy+y>=arrays[resource].shape[0] or sx+x>=arrays[resource].shape[1]:continue
                            tile=indices[y:y+8,x:x+8]
                            if not tile.any():continue
                            at=(sx+x,sy+y);cell_votes[resource].setdefault(at,Counter())[palkey]+=int(np.count_nonzero(tile))*w*h
    for resource,a in arrays.items():
        assert votes[resource],('No exact live material',resource)
        key=max(votes[resource],key=lambda k:(len(np.unique(palettes[k][1:])),votes[resource][k]));palette=palettes[key].astype('uint32')
        rgb=np.stack([(palette&31)*255//31,((palette>>5)&31)*255//31,((palette>>10)&31)*255//31],-1).astype('uint8')
        rgba=np.dstack([rgb[a],(a!=0).astype('uint8')*255]);rgba[a==0]=0
        cell_palettes={}
        for (x,y),choices in cell_votes[resource].items():
            selected=max(choices,key=lambda k:(len(np.unique(palettes[k][1:])),choices[k]));v=palettes[selected].astype('uint32')
            colors=np.stack([(v&31)*255//31,((v>>5)&31)*255//31,((v>>10)&31)*255//31],-1).astype('uint8');tile=a[y:y+8,x:x+8]
            rgba[y:y+8,x:x+8,:3]=colors[tile];rgba[y:y+8,x:x+8][tile==0]=0
            cell_palettes[f'{x},{y}']=v.tolist()
        image=Image.fromarray(rgba);image.save(folder/f'bank_{resource}_native.png')
        reference=Image.new('RGBA',(256,160));reference.paste(image,(0,0))
        reference.resize((768,480),Image.Resampling.NEAREST).save(folder/f'bank_{resource}_reference.png')
        items.append(dict(resource=resource,native_size=[a.shape[1],a.shape[0]],generation_size=[256,160],palette_native=palette.tolist(),palette_rgb=rgb.tolist(),palette_votes=votes[resource][key],cell_palettes=cell_palettes,output=f'bank_{resource}_generated.png'))
        card=Image.new('RGB',(768,420),'#25323c');thumb=image.resize((a.shape[1]*3,a.shape[0]*3),Image.Resampling.NEAREST);card.paste(thumb,(0,24),thumb);ImageDraw.Draw(card).text((4,3),str(resource),fill='white');cards.append(card)
    contact=Image.new('RGB',(1536,420*4),'#25323c')
    for i,card in enumerate(cards):contact.paste(card,(i%2*768,i//2*420))
    out=ROOT/'test_current/combat/mazinger_combination';contact.save(out/'banks_contact.png')
    (folder/'plan.json').write_text(json.dumps(dict(scope=__doc__,items=items),indent=2));print('Extracted',len(items),'exact live-palette banks')

if __name__=='__main__':main()
