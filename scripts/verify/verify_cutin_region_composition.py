"""Compare cached cut-in regions with full-canvas alpha on CPU and GPU."""
import json,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageChops
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from cutin_assets import CutinAssets
from gpu_surface import Surface

def main():
    assets=CutinAssets(ROOT,Image.open(ROOT/'graphics/kazuma_cutin_hd.png').convert('RGBA'),768)
    size=(768,576);visibility=np.full((192,256),255,dtype='uint8');visibility[12:97,80:143]=0
    mask=Image.fromarray(visibility);back=Image.new('RGB',size,(7,53,89));rows=[]
    for identifier in (6,7,90,107,171,172,174,175,177,178,180,181):
        image=assets[identifier];region,box=assets.region(identifier)
        for position in ((0,0),(-47,-21),(59,37)):
            viewport=Image.new('RGBA',size);viewport.paste(image,position)
            fullmask=ImageChops.multiply(mask.resize(size,Image.Resampling.NEAREST),viewport.getchannel('A'))
            expected=back.copy();expected.paste(viewport,(0,0),fullmask)
            left,upper=position[0]+box[0],position[1]+box[1];rect=(left,upper,left+region.width,upper+region.height)
            cpu=back.copy();cpu.paste(region,(left,upper),ImageChops.multiply(mask.resize(size,Image.Resampling.NEAREST).crop(rect),region.getchannel('A')))
            assert np.array_equal(np.asarray(cpu),np.asarray(expected)),(identifier,position,'CPU alpha changed')
            gpu=Surface(size);gpu.paste(back);gpu.draw(region,rect,mask=mask,mask_rect=(0,0,*size),alpha=True)
            error=int(np.abs(np.asarray(gpu.to_pil(),dtype='int16')-np.asarray(expected,dtype='int16')).max())
            assert error<=2,(identifier,position,'GPU alpha changed',error)
            rows.append(dict(cutin=identifier,position=position,cpu_exact=True,gpu_max_error=error,full_pixels=image.width*image.height,region_pixels=region.width*region.height))
    report=dict(scope=__doc__,cases=len(rows),rows=rows)
    (ROOT/'test_current/performance/cutin_region_equivalence.json').write_text(json.dumps(report,indent=2));print('Verified',len(rows),'CPU/GPU alpha cases')

if __name__=='__main__':main()
