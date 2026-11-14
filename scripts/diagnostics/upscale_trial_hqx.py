"""Add an hq4x (pixel-art scaler) panel to the upscale trial.

hq4x works on RGB only, so the sprite is scaled twice, over black and over
white; alpha comes from the difference of the two (difference matting) and
colour from the black-backed result divided by alpha. Writes
<image>_hq4x.png and zoom crops next to upscale_trial.py's output.
"""
import sys,types
sys.modules.setdefault('PIL.PyAccess',types.SimpleNamespace(PyAccess=object))   # type hints only in hqx
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import numpy as np
from PIL import Image,ImageDraw
import hqx


def hq4x_rgba(native):
    a=np.asarray(native.convert('RGBA'),dtype='float32');alpha=a[:,:,3:]/255
    over=lambda bg:Image.fromarray((a[:,:,:3]*alpha+bg*(1-alpha)).astype('uint8'))
    black=np.asarray(hqx.hq4x(over(0)),dtype='float32');white=np.asarray(hqx.hq4x(over(255)),dtype='float32')
    out_alpha=np.clip(1-(white-black).mean(2)/255,0,1)
    colour=np.where(out_alpha[:,:,None]>0.01,black/np.maximum(out_alpha[:,:,None],0.01),0)
    return Image.fromarray(np.dstack([np.clip(colour,0,255),out_alpha*255]).astype('uint8'),'RGBA')


def main():
    folder=ROOT/'test_current/parts/upscale_trial'
    images=[int(a) for a in sys.argv[1:]] or [1164,3392,21948]
    for image in images:
        native=Image.open(folder/f'{image}_native.png');out=hq4x_rgba(native);out.save(folder/f'{image}_hq4x.png');print(image,'hq4x',out.size)
    def strip(img,box,name):
        files=[f'{img}_native.png',f'{img}_current_hd.png',f'{img}_realesr-animevideov3.png',f'{img}_hq4x.png']
        tiles=[]
        for i,f in enumerate(files):
            im=Image.open(folder/f).convert('RGBA')
            if i==0:im=im.resize((im.width*4,im.height*4),Image.Resampling.NEAREST)
            c=im.crop(box);bg=Image.new('RGBA',c.size,(96,96,104,255));bg.alpha_composite(c);tiles.append(bg)
        W,H=tiles[0].size;s=Image.new('RGB',(W*4+12,H+18),(255,0,0));d=ImageDraw.Draw(s)
        for i,(t,l) in enumerate(zip(tiles,['native x4','current HD (imagegen)','ESRGAN animevideov3','hq4x'])):s.paste(t,(i*(W+4),18));d.text((i*(W+4)+2,2),l,fill=(255,255,255))
        if W<200:s=s.resize((s.width*2,s.height*2),Image.Resampling.LANCZOS)
        s.save(folder/name)
    strip(1164,(0,0,256,128),'hq_zoom_deathscythe_head.png')
    strip(1164,(640,0,1024,128),'hq_zoom_deathscythe_wing.png')
    strip(3392,(0,0,448,128),'hq_zoom_valstork.png')
    strip(21948,(0,128,400,256),'hq_zoom_effect_particles.png')


if __name__=='__main__':main()
