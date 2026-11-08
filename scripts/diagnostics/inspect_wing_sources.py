"""Inspect early IMG/PLT/PAT resources omitted by the PLT-first extractor."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import sys,json,struct
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,str(PROJECT_ROOT))
import scripts.assets.srw_graphics as g
ROOT=g.ROOT

def main():
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    rows=json.loads((ROOT/'test_current/rom_catalog/catalog.json').read_text())['records'];kinds={r['id']:r['kind'] for r in rows}
    out=ROOT/'test_current/parts';panels=[];records=[]
    for row in rows:
        i=row['id']
        if not (1150<=i<1260 and row['kind']=='IMG'):continue
        palette_id=next((j for j in range(i+1,i+4) if kinds.get(j)=='PLT'),None)
        if palette_id is None:continue
        indices=g.pixels(resource(i));pal=np.asarray(g.palette(resource(palette_id)),dtype='uint8')
        if indices.max()>=len(pal):continue
        rgba=pal[indices].copy();rgba[:,:,3]=(indices!=0)*255;atlas=Image.fromarray(rgba)
        pattern_id=next((j for j in range(palette_id+1,palette_id+3) if kinds.get(j)=='PAT'),None)
        pose=[]
        if pattern_id:
            data=resource(pattern_id);at=struct.unpack_from('<I',data,8)[0];n=struct.unpack_from('<H',data,at)[0];cursor=at+2
            for _ in range(n):
                flags=struct.unpack_from('<H',data,cursor)[0];cursor+=2;x=y=0
                if flags&0x2000:x,y=struct.unpack_from('<hh',data,cursor);cursor+=4
                tile=struct.unpack_from('<H',data,cursor)[0];cursor+=2
                if flags&0x4000:cursor+=4
                if flags&0x8000:cursor+=2
                tile&=4095;w=8<<(flags&3);h=8<<((flags>>2)&3);u=tile%32*8;v=tile//32*8
                if u+w>atlas.width or v+h>atlas.height:continue
                pose.append(dict(x=x,y=y,w=w,h=h,u=u,v=v,flags=flags))
        canvas=Image.new('RGBA',(256,192))
        for p in reversed(pose):
            art=atlas.crop((p['u'],p['v'],p['u']+p['w'],p['v']+p['h']))
            if p['flags']&16:art=art.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if p['flags']&32:art=art.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            canvas.alpha_composite(art,(128+p['x'],100+p['y']))
        atlas.save(out/f'wing_source_{i}.png');canvas.save(out/f'wing_pose_{i}.png')
        panel=Image.new('RGB',(256,270),(30,35,43));panel.paste(atlas,(0,20),atlas);panel.paste(canvas,(0,78),canvas);ImageDraw.Draw(panel).text((3,3),str((i,palette_id,pattern_id)),fill='white');panels.append(panel)
        records.append(dict(resource=i,palette=palette_id,pattern=pattern_id,poses=pose,native_size=list(atlas.size)))
    sheet=Image.new('RGB',(256*5,270*((len(panels)+4)//5)))
    for n,p in enumerate(panels):sheet.paste(p,(n%5*256,n//5*270))
    sheet.save(out/'wing_early_sources.png');(out/'wing_early_sources.json').write_text(json.dumps(records,indent=2));print(len(records))

if __name__=='__main__':main()
