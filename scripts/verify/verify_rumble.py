"""Live native battle, HD independence, output bounds and settings lifecycle."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import json,sys,subprocess
import numpy as np
from hd_core import Core,ROOT,HERE
from battle_rumble import BattleRumble
from player_rumble import PadRumble
OUT=ROOT/'test_current/combat'

def live(hd):
    core=Core(ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds',enabled=hd,demo=True)
    core.load(HERE/'demo.state',refresh_code=True);tracker=BattleRumble();events=[]
    inputs=json.loads((HERE/'demo_input.json').read_text())
    for frame in range(64700,68001):
        core.buttons={e['button'] for e in inputs if e['from']<=frame<e['to']};core.run();core.audio.clear()
        effect=tracker.sample(core)
        if effect:events.append(dict(frame=frame,**effect))
        if hd and frame==65600:core.save(OUT/'rumble_contact.state')
    core.close();(OUT/f'rumble_hd_{int(hd)}.json').write_text(json.dumps(events,indent=2))

class FakePad:
    def __init__(self,supported=True):self.calls=[];self.stops=0;self.supported=supported
    def rumble(self,low,high,duration):self.calls.append((low,high,duration));return self.supported
    def stop_rumble(self):self.stops+=1

def output_checks():
    r=PadRumble();p=FakePad();assert r.play(p,True,50,low=.6,high=.8,duration=110)
    assert p.calls==[(.3,.4,110)]
    assert not r.play(p,False,50) and p.stops==1
    assert not r.play(None,True,50)
    assert not r.play(FakePad(False),True,50)
    r.play(p,True,100,low=8,high=-3,duration=0);assert p.calls[-1]==(1,0,20)
    q=FakePad();r.play(q,True,100,duration=99999);assert q.calls[-1][2]==600 and p.stops>=2
    r.stop();assert q.stops==1

def ui_checks():
    import tkinter as tk
    from tkinter import ttk
    from types import SimpleNamespace
    from hd_emulator import EmulatorWindow
    from player_controls import read_settings
    root=tk.Tk();root.withdraw()
    args=SimpleNamespace(config=OUT/'rumble_ui_settings.json',save_root=OUT/'rumble_ui_saves',no_start=True,demo=False,rom=None,state=None,state_frame=64700,paused=True)
    app=EmulatorWindow(root,args)
    def descendants(widget):
        for child in widget.winfo_children():yield child;yield from descendants(child)
    try:
        app.pad=FakePad();app.rumble_dialog();app.dialog.withdraw()
        controls=list(descendants(app.dialog));test=next(w for w in controls if isinstance(w,ttk.Button) and w.cget('text')=='진동 테스트');test.invoke()
        assert app.pad.calls,'settings test did not reach the selected device'
        scale=next(w for w in controls if isinstance(w,ttk.Scale));scale.set(40)
        next(w for w in controls if isinstance(w,ttk.Button) and w.cget('text')=='적용').invoke()
        assert read_settings(args.config)['rumble_strength']==40 and app.pad.stops
        app.rumble.play(app.pad,True,50);app.focus_lost(None);assert app.rumble.device is None
        app.loaded=True;app.paused=False;app.rumble.play(app.pad,True,50);app.toggle_pause();assert app.rumble.device is None
        app.rumble.play(app.pad,True,50);app.stop_worker();assert app.rumble.device is None
    finally:app.close()

def main():
    if '--live' in sys.argv:live('--hd' in sys.argv);return
    OUT.mkdir(exist_ok=True)
    if '--recorded' not in sys.argv:
        for mode in (False,True):subprocess.run([sys.executable,__file__,'--live']+(['--hd'] if mode else []),check=True,stdout=subprocess.DEVNULL)
    off=json.loads((OUT/'rumble_hd_0.json').read_text());on=json.loads((OUT/'rumble_hd_1.json').read_text())
    impacts=[e for e in on if e.get('reason')=='impact_flash']
    beams=[e for e in on if e.get('reason')=='beam_stream']
    assert impacts==[e for e in off if e.get('reason')=='impact_flash'],'HD changed impact timing'
    assert on==off,'HD changed energy feedback'
    with np.load(OUT/'battle_feedback.npz') as archive:
        states=archive['states'];start=int(archive['start'])
    assert all(states[e['frame']-start,0]==128 and states[e['frame']-start,1]==0 for e in off+on if e['duration'])
    assert len(impacts)==16 and impacts[0]['frame']==65668
    assert any(e['repeated'] for e in impacts)
    assert beams and all(e['duration']==110 and e['high']==1. and e['low']>=.65 for e in beams)
    assert all(65668<=e['frame']<=66102 for e in impacts),'rumble during non-hit preview segment'
    assert on[-1]['duration']==0 and on[-1]['reason']=='battle_end'
    coverage_checks();output_checks();ui_checks();worker_checks()
    report=dict(native_hit_pulses=len(impacts),native_beam_pulses=len(beams),beam_pulse_ms=110,first_hit=impacts[0]['frame'],last_hit=impacts[-1]['frame'],hd_independent_all_events=True,all_16_hit_palette_banks=True,native_oam_energy_detection=True,non_battle_segments_silent=True,battle_end_stops=True,device_output_bounds=True,unsupported_device_safe=True,settings_test_button=True,persistent_strength=True,pause_focus_session_stop=True,worker_hit_event=True,physical_gamepad_tested=False,all_weapons_replayed=False)
    (OUT/'rumble_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))

def coverage_checks():
    from beam_rumble import BeamObserver
    for bank in range(16):
        tracker=BattleRumble();pal=np.full((16,16),8|(8<<5)|(8<<10),dtype='uint16')
        attrs=np.zeros((128,4),dtype='uint16');attrs[:,0]=512;attrs[0]=[40,40,bank<<12,0]
        for _ in range(35):assert tracker.observe(True,pal,attrs) is None
        pal[bank,1:]=32767
        assert tracker.observe(True,pal,attrs)['reason']=='impact_flash',bank
        for _ in range(10):assert tracker.observe(False,pal,attrs) is None or not tracker.was_active
    for color in (31,32767,31<<5,(31<<5)|(31<<10)):
        palette=np.zeros(16,dtype='uint16');palette[1]=color
        thin=np.zeros((16,64),dtype='uint8');thin[6:10,2:62]=1
        assert BeamObserver.classify(thin,palette),color
    square=np.ones((32,32),dtype='uint8');palette[1]=32767
    assert not BeamObserver.classify(square,palette),'white armor classified as a beam'
def worker_checks():
    from scripts.verify.verify_player import Session
    session=Session(state=OUT/'rumble_contact.state',state_frame=65601)
    try:
        session.until('loaded');session.until('frame');session.send('pause',value=False);session.until('paused')
        event=session.until('rumble')
        while event.get('reason')!='impact_flash':event=session.until('rumble')
        assert event['duration']>0
        session.send('pause',value=True);session.until('paused')
        assert any(e['event']=='rumble' and e['duration']==0 for e in session.events)
    finally:session.close()

if __name__=='__main__':main()
