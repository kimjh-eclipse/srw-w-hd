"""Compare assembled silhouettes at actual captured OAM positions."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw
from hd_parts import PartsRenderer,SCALE,ROOT

def assembled(renderer,parts,oam):
    result=Image.new('RGBA',(1440,1080))
    active=[i for i in range(128) if parts[i,0]]
    for i in sorted(active,key=lambda n:(((int(parts[n,3])>>10)&3),n),reverse=True):
        row=parts[i].copy();row[5]=0
        art=renderer.sprite(row,oam);a,b=map(int,row[1:3]);x=b&511;y=a&255
        if x>=256:x-=512
        if y>=192:y-=256
        result.alpha_composite(art,(round(x*SCALE),round(y*SCALE)))
    return result

def verify():
    out=ROOT/'test_current/parts';baseline=PartsRenderer();native=PartsRenderer();corrected=PartsRenderer();report={};panels=[]
    for frame in (65520,65880):
        data=np.load(out/f'data_{frame}.npz');parts=data['parts'];oam=data['oam'].tobytes()
        for row in parts:
            binding=int(row[0])
            if not binding:continue
            spec=baseline.bindings[binding-1];x,y,w,h=[spec[k] for k in ('x','y','w','h')]
            baseline.prepared[binding]=baseline.atlas.crop((x*8,y*8,(x+w)*8,(y+h)*8))
            native.prepared[binding]=native.native_atlas.crop((x,y,x+w,y+h)).resize((w*8,h*8),Image.Resampling.LANCZOS)
        old=assembled(baseline,parts,oam);new=assembled(corrected,parts,oam);reference=assembled(native,parts,oam)
        a,b,c=[np.asarray(im.getchannel('A')) for im in (old,new,reference)]
        solid=c>=230;empty=c<=16
        metrics=dict(opaque_reference_pixels=int(solid.sum()),gaps_before=int((solid&(a<128)).sum()),gaps_after=int((solid&(b<128)).sum()),
                     overhang_before=int((empty&(a>=128)).sum()),overhang_after=int((empty&(b>=128)).sum()))
        assert metrics['gaps_after']<=metrics['gaps_before'],metrics
        assert metrics['overhang_after']<=metrics['overhang_before'],metrics
        report[str(frame)]=metrics
        bbox=reference.getbbox();x0,y0,x1,y1=bbox;box=(max(x0-12,0),max(y0-12,0),min(x1+12,1440),min(y1+12,1080))
        panel=Image.new('RGB',(1000,440),(24,28,36));draw=ImageDraw.Draw(panel)
        for index,(label,im) in enumerate([('BEFORE',old),('ALIGNED',new),('NATIVE SHAPE',reference)]):
            crop=im.crop(box);crop.thumbnail((320,390));panel.paste(crop,(index*333+(333-crop.width)//2,35),crop)
            draw.text((index*333+15,10),label,fill='white')
        panels.append(panel)
    stats=list(corrected.registration_stats.values())
    report['prepared_parts']=len(stats);report['reference_fill_pixels']=sum(s['reference_fill_pixels'] for s in stats)
    report['edge_extension_pixels']=sum(s['filled_edge_pixels'] for s in stats)
    (out/'alignment_verification.json').write_text(json.dumps(report,indent=2))
    sheet=Image.new('RGB',(1000,440*len(panels)))
    for i,panel in enumerate(panels):sheet.paste(panel,(0,440*i))
    sheet.save(out/'alignment_comparison.png');print(json.dumps(report))

if __name__=='__main__':verify()
