"""Verify observed matching, protected HUD, alpha and bounded texture cache."""
import json,time
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
from hd_portraits import PortraitRenderer
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'test_current/portrait';OUT.mkdir(exist_ok=True)
def main():
    renderer=PortraitRenderer(async_prepare=False);plans=[]
    for p in ('observed.json','observed_extra.json'):
        plans.extend(json.loads((ROOT/'graphics/portraits'/p).read_text())['portraits'])
    results=[];review=Image.new('RGB',(672,108*len(plans)),'#202830');draw=ImageDraw.Draw(review)
    for k,item in enumerate(plans):
        name=item['name'];native=np.zeros((384,256,3),dtype='uint8');x,y,w,h=item['rectangle']
        original=Image.open(ROOT/'graphics/portraits'/(name+'_native.png')).convert('RGB');native[y:y+h,x:x+w]=np.asarray(original)
        base=Image.fromarray(native[:192]).resize((1440,1080),Image.Resampling.NEAREST);before=np.asarray(base).copy()
        assert renderer.compose(base,native),name;assert renderer.last_match==name,(name,renderer.last_match)
        after=np.asarray(base);changed=np.any(after!=before,axis=2)
        # All game text and all pixels outside the portrait box stay identical.
        allowed=np.zeros(changed.shape,dtype=bool);allowed[round(y*1080/192):round((y+h)*1080/192),round(x*1440/256):round((x+w)*1440/256)]=True
        assert not np.any(changed&~allowed),name
        yy=round(y*1080/192);assert not changed[yy].any(),name
        assert changed.sum()>20000,name
        review.paste(original.resize((112,96),Image.Resampling.NEAREST),(0,k*108))
        review.paste(base.crop((0,yy,315,yy+270)).resize((112,96)),(116,k*108));draw.text((236,k*108+36),name,fill='white')
        results.append(dict(name=name,match=renderer.last_match,changed_pixels=int(changed.sum())))
    native[:]=0;assert not renderer.compose(base,native)
    status=OUT/'status_native.png'
    if status.exists():
        native[:192]=np.asarray(Image.open(status).convert('RGB'))
        status_top=Image.fromarray(native[:192]).resize((1440,1080),Image.Resampling.NEAREST)
        assert renderer.compose(status_top,native) and renderer.last_match=='kazuma'
        assert renderer.last_rectangle==(0,24,56,48)
        status_top.save(OUT/'status_hd.png')
    for key,entries in renderer.groups.items():
        for candidates in entries.values():
            for item in candidates:renderer._art(item)
    assert len(renderer.cache)<=32
    portrait=np.asarray(Image.open(ROOT/'graphics/portraits/mao_native.png').convert('RGB'));native[136:184,:56]=portrait
    start=time.perf_counter()
    for _ in range(300):renderer.compose(base,native)
    ms=(time.perf_counter()-start)*1000/300
    review.save(OUT/'in_game_comparison.png');report=dict(observed=results,registered=len(renderer.items),cache_size=len(renderer.cache),compose_ms=round(ms,3))
    (OUT/'verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
