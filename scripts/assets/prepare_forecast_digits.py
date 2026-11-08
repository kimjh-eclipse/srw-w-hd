"""Compile the large hit-rate font from its real PAT flips and IMG pieces."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
from scripts.assets import srw_graphics as g
import struct,json,hashlib
import numpy as np
from PIL import Image,ImageDraw

def main():
    rom=(ROOT/'baseline/SRWW_Korean_1.0.8.nds').read_bytes();offsets=g.archive(rom)
    def resource(i):return g.decompress(rom[g.BASE+offsets[i]:g.BASE+offsets[i+1]])
    image=g.pixels(resource(4309));pattern=resource(4310);glyphs=[]
    for pose in list(range(10))+[12]:
        at=struct.unpack_from('<I',pattern,8+4*pose)[0];count=struct.unpack_from('<H',pattern,at)[0];at+=2;canvas=np.zeros((16,16),dtype='uint8');pieces=[]
        for _ in range(count):
            flags=struct.unpack_from('<H',pattern,at)[0];at+=2;x=y=0
            if flags&0x2000:x,y=struct.unpack_from('<hh',pattern,at);at+=4
            tile=struct.unpack_from('<H',pattern,at)[0]&4095;at+=2
            if flags&0x4000:at+=4
            if flags&0x8000:at+=2
            w=8<<(flags&3);h=8<<((flags>>2)&3);sx=tile%32*8;sy=tile//32*8
            a=image[sy:sy+h,sx:sx+w]
            if flags&0x100:a=np.fliplr(a)
            if flags&0x200:a=np.flipud(a)
            pieces.append((x,y,w,h,a))
        for x,y,w,h,a in reversed(pieces):
            region=canvas[y:y+h,x:x+w];region[a>0]=a[a>0]
        glyphs.append(canvas)
    chars=np.array(list('0123456789%'));glyphs=np.asarray(glyphs)
    np.savez_compressed(ROOT/'graphics/fonts/forecast_glyphs.npz',indices=glyphs,characters=chars)
    info=dict(image_resource=4309,pattern_resource=4310,characters='0123456789%',cell=[16,16],source_sha256=hashlib.sha256(resource(4309)+resource(4310)).hexdigest())
    (ROOT/'graphics/fonts/forecast_glyphs.json').write_text(json.dumps(info,indent=2))
    out=Image.new('RGB',(11*80,80))
    for i,a in enumerate(glyphs):
        pixels=np.repeat(((a>1)*255).astype('uint8')[:,:,None],3,axis=2);out.paste(Image.fromarray(pixels).resize((80,80),Image.Resampling.NEAREST),(i*80,0))
    out.save(ROOT/'test_current/font/forecast_digits_reference.png');print(info)

if __name__=='__main__':main()
