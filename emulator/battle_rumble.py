"""Observe active native OBJ hit palettes and energy textures in battle."""
import ctypes as C
import numpy as np
from beam_rumble import BeamObserver
from background_rumble import BackgroundEnergyObserver

class BattleRumble:
    def __init__(self):
        self.palette=np.zeros((16,16),dtype='uint16');self.oam=np.zeros((128,4),dtype='uint16')
        self.registers=np.zeros(64,dtype='uint16');self.beams=BeamObserver();self.background=BackgroundEnergyObserver()
        self.bgpalette=np.zeros((16,16),dtype='uint16');self.engine=0;self.enhanced=False;self.reset();self.ram=None
    def reset(self):
        self.previous=None;self.age=0;self.tick=0;self.last_hit=-100;self.last_beam=-100;self.beam_visible=False;self.was_active=False
        self.last_energy=-100;self.last_orb_token=None;self.orb_changed=False;self.bg_visible=False;self.background.reset()
    def observe(self,active,palette,oam,beam=False,orb=False,background=False):
        if not active:
            stopped=self.was_active;self.reset()
            return dict(duration=0,reason='battle_end') if stopped else None
        self.was_active=True;self.age+=1;self.tick+=1
        colors=np.asarray(palette[:,1:],dtype='uint32')
        rgb=np.stack([colors&31,(colors>>5)&31,(colors>>10)&31],-1).astype('float32')
        light=rgb.mean((1,2));previous=self.previous;self.previous=light
        if previous is None or self.age<30:return None
        attrs=np.asarray(oam,dtype='uint16');a,b,c=attrs[:,:3].T
        y=a&255;x=b&511;pal=c>>12
        visible=((a&0x300)!=0x200)&((a>>14)!=3)&(((a>>10)&3)<2)&(y<120)&((x<256)|(x>448))
        used=np.array([np.any(visible&(pal==i)) for i in range(16)])
        pulse=(light>=25)&(previous>=5)&(light-previous>=5)&used
        if pulse.any() and self.tick-self.last_hit>=5:
            repeated=self.tick-self.last_hit<=24;self.last_hit=self.tick
            return dict(low=.9 if repeated else 1.,high=1.,duration=95 if repeated else 155,reason='impact_flash',repeated=repeated)
        if background and self.tick-self.last_energy>=8:
            self.last_energy=self.tick;self.last_hit=self.tick
            return dict(low=1.,high=1.,duration=180,reason='background_explosion',repeated=True)
        if orb and self.tick-self.last_hit>=6 and self.tick-self.last_energy>=6:
            self.last_energy=self.tick
            return dict(low=.85,high=1.,duration=125,reason='energy_orb',repeated=True)
        if beam and self.tick-self.last_hit>=8 and self.tick-self.last_beam>=4:
            self.last_beam=self.tick
            # Overlapping pulses let physical motors spin up despite IPC latency.
            # Modulate the heavy motor for a buzz rather than isolated taps.
            return dict(low=.9 if (self.tick//4)%2 else .65,high=1.,duration=110,reason='beam_stream',repeated=True)
        return None
    def sample(self,core):
        if not core.clean_korean:return None
        if self.ram is None:
            core.api.retro_get_memory_data.argtypes=[C.c_uint];core.api.retro_get_memory_data.restype=C.c_void_p
            self.ram=core.api.retro_get_memory_data(2)
            core.api.retro_srw_copy_obj_debug.argtypes=[C.c_void_p,C.c_void_p,C.c_void_p]
            self.enhanced=hasattr(core.api,'retro_srw_copy_effect_debug')
            if self.enhanced:core.api.retro_srw_copy_effect_debug.argtypes=[C.c_void_p]*4
        active=C.c_uint32.from_address(self.ram+0xa6f38).value==128 and C.c_uint32.from_address(self.ram+0x1e7a10).value==0
        if not active:return self.observe(False,self.palette,self.oam)
        if self.enhanced:
            self.engine=int(core.api.retro_srw_copy_effect_debug(self.oam.ctypes.data,self.palette.ctypes.data,self.bgpalette.ctypes.data,self.registers.ctypes.data))-1
        else:core.api.retro_srw_copy_obj_debug(self.oam.ctypes.data,self.palette.ctypes.data,self.registers.ctypes.data)
        if self.tick%2==0:
            self.beam_visible=self.beams.active(core,self.oam,self.palette,self.registers,max(0,self.engine))
            token=self.beams.orb_token
            self.orb_changed=self.beams.orb_active and token!=self.last_orb_token
            self.last_orb_token=token
            self.bg_visible=self.background.sample(core,self.bgpalette,self.registers) if self.enhanced else False
        return self.observe(True,self.palette,self.oam,self.beam_visible,self.orb_changed,self.bg_visible)
