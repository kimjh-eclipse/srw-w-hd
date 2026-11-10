"""Round OBJ/BG energy detection, idle rejection and real native HD parity."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT
import ctypes as C,json,time
from collections import Counter
from types import SimpleNamespace
import numpy as np
from beam_rumble import BeamObserver
from background_rumble import BackgroundEnergyObserver
from battle_rumble import BattleRumble
from hd_core import Core

def synthetic():
    palette=np.zeros(256,dtype='uint16');palette[1]=31|(31<<5)|(31<<10);palette[2]=31<<5
    yy,xx=np.ogrid[:32,:32];orb=np.where((xx-16)**2+(yy-16)**2<13**2,2,0).astype('uint8')
    assert BeamObserver.classify_orb(orb,palette)
    assert not BeamObserver.classify_orb(np.zeros_like(orb),palette)
    assert BeamObserver.classify_white_orb(np.where(orb,1,0),palette),'Round white energy must be covered'
    assert not BeamObserver.classify_white_orb(np.ones_like(orb),palette),'Solid white armor rectangle is not a round orb'
    ordered=orb.reshape(4,8,4,8).transpose(0,2,1,3).reshape(-1)
    packed=(ordered[::2]|ordered[1::2]<<4).astype('uint8')
    def copy_obj(address,target,length):C.memmove(target,packed.ctypes.data,length);return 1
    obj_core=SimpleNamespace(api=SimpleNamespace(retro_srw_copy_vram=copy_obj))
    attrs=np.zeros((128,4),dtype='uint16');attrs[:,0]=512;attrs[0]=[20|1024,20|(2<<14),0,0]
    obj_palette=np.zeros((16,16),dtype='uint16');obj_palette[0,2]=31<<5
    obj_regs=np.zeros(64,dtype='uint16');obj_regs[0]=16
    observer=BeamObserver();assert not observer.active(obj_core,attrs,obj_palette,obj_regs)
    assert observer.orb_active,'Translucent round energy OBJ was missed'
    attrs[0,0]=20;observer.active(obj_core,attrs,obj_palette,obj_regs)
    assert not observer.orb_active,'Opaque armor triggered round-energy feedback'
    maps=np.full(1024,1,dtype='<u2');tiles=np.zeros(32768,dtype='uint8');regs=np.zeros(64,dtype='uint16')
    class API:
        def retro_srw_copy_vram(self,address,target,length):
            source=maps if address==0x06010000 else tiles
            C.memmove(target,source.ctypes.data,length);return 1
    core=SimpleNamespace(api=API(),bg_layout=[(0,0,0,0,0,256,256,0,0),(0,0x06010000,0x06000000,0,0,256,256,1,1)])
    tracker=BackgroundEnergyObserver();assert not tracker.sample(core,palette,regs)
    tiles[32:64]=0x22
    assert tracker.sample(core,palette,regs),'A newly appearing dense BG energy effect must trigger'
    assert not tracker.sample(core,palette,regs),'A static energy image must not repeatedly trigger'
    core.bg_layout[1]=(0,0x06010000,0x06000000,37,18,256,256,1,1)
    assert not tracker.sample(core,palette,regs),'Scrolling unchanged art must not trigger'
    palette[200]=1234
    assert not tracker.sample(core,palette,regs),'An unused UI palette color must not trigger'
    regs[0x50//2]=2<<6;regs[0x54//2]=12
    assert tracker.sample(core,palette,regs),'Native BG whiteout should trigger once'
    assert not tracker.sample(core,palette,regs)
    state=BattleRumble();oam=np.zeros((128,4),dtype='uint16');pal=np.zeros((16,16),dtype='uint16')
    for _ in range(32):state.observe(True,pal,oam)
    assert state.observe(True,pal,oam,orb=True)['reason']=='energy_orb'
    for _ in range(8):state.observe(True,pal,oam)
    assert state.observe(True,pal,oam,background=True)['reason']=='background_explosion'
    assert state.observe(False,pal,oam)['duration']==0
    return dict(round_obj=True,new_bg_energy=True,whiteout=True,static_and_camera_rejected=True,unused_palette_rejected=True,battle_end_stops=True)

def main():
    checks=synthetic();rows=[]
    c=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',demo=True,user_dir=ROOT/'test_current/combat/energy_saves')
    try:
        assert hasattr(c.api,'retro_srw_copy_effect_debug'),'Updated native bridge required'
        for scene,state,frames in [('plasma','named_attacks/plasma_360',1000),('eid','eid_firing',600),('bonta','bonta_attack',900)]:
            versions=[];costs=[]
            for enabled in (False,True):
                c.enabled=enabled;c.api.retro_srw_set_hd_enabled(int(enabled));c.load(ROOT/f'test_current/combat/{state}.state')
                tracker=BattleRumble();events=[]
                for frame in range(frames):
                    c.run();c.audio.clear();start=time.perf_counter();effect=tracker.sample(c);costs.append((time.perf_counter()-start)*1000)
                    if effect:events.append(dict(frame=frame,**effect))
                    c.buttons={11,8} if frame%120<5 else set()
                c.buttons=set();versions.append(events)
            assert versions[0]==versions[1],(scene,'HD changed effect detection')
            counts=Counter(e['reason'] for e in versions[1])
            if scene=='plasma':assert counts['background_explosion']>0,(scene,counts)
            rows.append(dict(scene=scene,hd_parity=True,events=dict(counts),median_ms=float(np.median(costs)),p95_ms=float(np.percentile(costs,95)),timeline=versions[1]))
            print(scene,dict(counts),flush=True)
    finally:c.close()
    report=dict(synthetic=checks,scenes=rows,physical_strength_subjective=False)
    (ROOT/'test_current/combat/energy_rumble_verification.json').write_text(json.dumps(report,indent=2))

if __name__=='__main__':main()
