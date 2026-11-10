"""Detect changing dense BG energy and white flashes from native VRAM only.

Viewport sampling is 4x4 pixels, capped at three text BG layers. Unchanged
textures/palettes never trigger from scrolling alone. No HD image decoding.
"""
import ctypes as C
import zlib
import numpy as np
from beam_rumble import BeamObserver

class BackgroundEnergyObserver:
    def __init__(self):
        self.maps=np.empty(8192,dtype='uint8');self.tiles=np.empty(65536,dtype='uint8')
        self.previous={};self.flash=None
        self.x=np.arange(2,256,4)[None,:];self.y=np.arange(2,120,4)[:,None]

    def reset(self):self.previous.clear();self.flash=None

    @staticmethod
    def measure(indices,palette):
        lookup=BeamObserver.energy_table(palette);lookup[0]=False
        mask=lookup[indices];count=int(mask.sum())
        if count<64:return count,False
        # Dense 24px energy cores; isolated stars, thin grid lines and the
        # small bright details of a robot do not form such a patch.
        integral=np.pad(mask.astype('int32'),((1,0),(1,0))).cumsum(0).cumsum(1)
        patches=integral[6:,6:]-integral[:-6,6:]-integral[6:,:-6]+integral[:-6,:-6]
        return count,bool(patches.size and patches.max()>=26)

    def sample(self,core,palette,registers):
        cnt=int(registers[0x50//2]);fade=min(int(registers[0x54//2])&31,16) if (cnt>>6)&3==2 else 0
        master=int(registers[0x6c//2]);white=min(master&31,16) if master>>14==1 else 0
        levels=(fade,white);old=self.flash;self.flash=levels
        flash=old is not None and any(now-before>=3 for now,before in zip(levels,old))
        event=flash
        for layer,info in enumerate(core.bg_layout):
            if layer==0 or not info[7] or info[5] not in (256,512) or info[6] not in (256,512):continue
            eight=bool(info[0]&128);tile_bytes=65536 if eight else 32768
            map_bytes=info[5]*info[6]//32
            if not core.api.retro_srw_copy_vram(info[1],self.maps.ctypes.data,map_bytes):continue
            if not core.api.retro_srw_copy_vram(info[2],self.tiles.ctypes.data,tile_bytes):continue
            stamp=(zlib.crc32(self.maps[:map_bytes]),zlib.crc32(self.tiles[:tile_bytes]),zlib.crc32(palette))
            previous=self.previous.get(layer)
            if previous is not None and previous[0][:3]==stamp:continue
            gx=(self.x+info[3])%info[5];gy=(self.y+info[4])%info[6]
            address=((gy//256)*(info[5]//256)+gx//256)*1024+(gy%256//8)*32+gx%256//8
            entries=self.maps[:map_bytes].view('<u2')[address]
            px=np.broadcast_to(gx%8,entries.shape);py=np.broadcast_to(gy%8,entries.shape)
            px=np.where(entries&1024,7-px,px);py=np.where(entries&2048,7-py,py)
            tile=entries&1023;pixel=py*8+px
            if eight:
                indices=self.tiles[tile*64+pixel].astype('uint16')
            else:
                packed=self.tiles[tile*32+pixel//2]
                local=np.where(pixel&1,packed>>4,packed&15)
                indices=np.where(local,local+(entries>>12)*16,0)
            count,dense=self.measure(indices,palette.reshape(-1))
            used=np.unique(indices);used=used[used!=0]
            stamp=stamp+(zlib.crc32(palette.reshape(-1)[used]),)
            self.previous[layer]=(stamp,count)
            if previous is None:continue
            grew=count>=previous[1]*1.15+12
            recolored=stamp[3]!=previous[0][3] and count>=previous[1]*.8
            if dense and (grew or recolored):event=True
        return bool(event)
