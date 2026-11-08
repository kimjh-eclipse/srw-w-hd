"""Pack only the remaining named-unit fragments, preserving native UVs."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
import json,struct
import numpy as np
from PIL import Image

def main():
    folder=ROOT/'graphics/named_variants';folder.mkdir(exist_ok=True)
    target=folder/'plan.json'
    if target.exists():print('Existing immutable plan retained');return
    report=json.loads((ROOT/'test_current/parts/named_variant_linking.json').read_text())
    roster=json.loads((ROOT/'test_current/parts/named_unit_catalog.json').read_text());units={u['unit_id']:u for u in roster['units']}
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    sheets=[];segments=[];canvas=Image.new('RGBA',(256,256));x=y=row=4
    def flush():
        nonlocal segments,canvas,x,y,row
        if not segments:return
        name=f'named_variant_{len(sheets):02}'
        canvas.save(folder/(name+'_native.png'));canvas.resize((1024,1024),Image.Resampling.NEAREST).save(folder/(name+'_reference.png'))
        sheets.append(dict(name=name,native_size=[256,256],image=name+'_hd.png',reference=name+'_reference.png',segments=segments))
        segments=[];canvas=Image.new('RGBA',(256,256));x=y=row=4
    for p in sorted(report['unresolved_parts'],key=lambda p:(-p['h'],-p['w'],p['image'],p['hash'])):
        if x+p['w']+4>256:x=4;y+=row+4;row=4
        if y+p['h']+4>256:flush()
        uid=p['unit_ids'][0];palid=struct.unpack_from('<H',rom,0x716d8+uid*40+10)[0]
        colors=np.frombuffer(resource(palid)[8:],dtype='<u2');colors=colors[p['bank']*16:(p['bank']+1)*16]
        if len(colors)<16:colors=np.frombuffer(resource(palid)[8:],dtype='<u2')[:16]
        palette=np.stack([(colors&31)*255//31,((colors>>5)&31)*255//31,((colors>>10)&31)*255//31],1).astype('uint8')
        a=g.pixels(resource(p['image']))[p['y']:p['y']+p['h'],p['x']:p['x']+p['w']]
        patch=Image.fromarray(np.dstack([palette[a],(a!=0).astype('uint8')*255]));canvas.paste(patch,(x,y))
        segments.append(dict(**p,atlas_x=x,atlas_y=y,palette_rgb=palette.tolist(),name_ja=units[uid]['name_ja'],name_ko=units[uid]['name_ko']))
        x+=p['w']+4;row=max(row,p['h'])
    flush();target.write_text(json.dumps(dict(scope='Exact named-unit primary fragments left after proven HD reuse',sheets=sheets),ensure_ascii=False,indent=2),encoding='utf-8')
    print('sheets',len(sheets),'parts',sum(len(s['segments']) for s in sheets))

if __name__=='__main__':main()
