"""Read native OBJ energy artwork, independent of HD replacement and audio."""
from collections import OrderedDict
import ctypes as C
import numpy as np

class BeamObserver:
    WIDTHS=((8,16,32,64),(16,32,32,64),(8,8,16,32))
    HEIGHTS=((8,16,32,64),(8,8,16,32),(16,32,32,64))
    def __init__(self):self.cache=OrderedDict();self.raw=np.empty(8192,dtype='uint8');self.bound=False

    @staticmethod
    def energy_table(palette):
        p=np.asarray(palette,dtype='uint16');r=p&31;g=(p>>5)&31;b=(p>>10)&31
        return ((g>=24)&(g>=r+5)&(g+5>=b))|((g>=25)&(b>=25)&(r<=19))|((b>=27)&(r<=18)&(g>=15))|((r>=28)&(g>=27)&(b<=19))|((r>=27)&(b>=27)&(g<=18))|((r>=28)&(g<=22)&(b<=18))|((r>=28)&(g>=28)&(b>=28))

    @staticmethod
    def classify(indices,palette):
        lookup=BeamObserver.energy_table(palette);lookup[0]=False;mask=lookup[indices]
        ys,xs=np.nonzero(mask)
        if len(xs)<24:return False
        width=int(xs.max()-xs.min()+1);height=int(ys.max()-ys.min()+1)
        if width<10:return False
        # Small saturated green emitters and long horizontal energy streams.
        colors=np.asarray(palette,dtype='uint16')[indices[mask]];r=colors&31;g=(colors>>5)&31;b=(colors>>10)&31
        green=int(np.count_nonzero((g>=25)&(r<=18)&(b<=25)))
        opaque=int(np.count_nonzero(indices))
        saturated=(np.maximum.reduce([r,g,b])-np.minimum.reduce([r,g,b]))>=8
        stream=width>=max(18,height*2.5) and int(mask.sum(1).max())>=12
        # Broad white armor is common; only a dense, very thin white core
        # qualifies without a saturated energy color around it.
        if np.count_nonzero(saturated)<24:
            stream=width>=max(24,height*4) and len(xs)>=opaque*.8
        return stream or (green>=max(24,opaque*.55) and 10<=width<=24 and 4<=height<=24)

    def active(self,core,oam,palette,registers):
        if not self.bound:
            core.api.retro_srw_copy_vram.argtypes=[C.c_uint,C.c_void_p,C.c_uint];self.bound=True
        disp=int(registers[0])|(int(registers[1])<<16);one_d=bool(disp&16);boundary=5+((disp>>20)&3) if one_d else 5
        # Native owners exclude sprites suppressed for HD replacement. Read OAM
        # directly so enabling HD cannot disable weapon feedback.
        eligible=self.energy_table(palette);eligible[:,0]=False
        banks=eligible.any(axis=1)
        for index,(a,b,c,_) in enumerate(np.asarray(oam,dtype='uint16')):
            a,b,c=int(a),int(b),int(c);shape=a>>14;size=b>>14
            if shape==3 or ((a>>10)&3)>=2 or (not a&256 and a&512):continue
            x=b&511;y=a&255;x=x-512 if x>=256 else x;y=y-256 if y>=192 else y
            w,h=self.WIDTHS[shape][size],self.HEIGHTS[shape][size]
            if x>=256 or y>=120 or x+w*2<=0 or y+h*2<=0:continue
            eight=bool(a&8192)
            if eight and disp&0x80000000:continue
            if not (banks.any() if eight else banks[c>>12]):continue
            colors=palette.reshape(-1) if eight else palette[c>>12]
            tile_bytes=64 if eight else 32;stride=w//8*tile_bytes if one_d else 1024
            length=(h//8-1)*stride+w//8*tile_bytes
            base=0x06400000+((c&1023)<<boundary)
            core.api.retro_srw_copy_vram(base,self.raw.ctypes.data,length)
            data=self.raw[:length].tobytes();key=(w,h,eight,stride,data,colors.tobytes())
            found=self.cache.pop(key,None)
            if found is None:
                tiles=np.stack([self.raw[row*stride:row*stride+w//8*tile_bytes] for row in range(h//8)])
                if eight:indices=tiles.reshape(h//8,w//8,8,8)
                else:
                    pairs=np.stack((tiles&15,tiles>>4),axis=-1)
                    indices=pairs.reshape(h//8,w//8,8,8)
                indices=indices.transpose(0,2,1,3).reshape(h,w)
                found=self.classify(indices,colors)
            self.cache[key]=found
            while len(self.cache)>96:self.cache.popitem(last=False)
            if found:return True
        return False
