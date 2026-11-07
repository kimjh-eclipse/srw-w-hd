"""Action bindings, focus behavior, display parity and real worker speed."""
import argparse,json,time,threading
from types import SimpleNamespace
import numpy as np
from PIL import Image
from player_controls import read_settings,screen_rectangles
from player_worker import TOP_BYTES,BOTTOM_BYTES,FRAME_BYTES
from verify_player import Session,OUT,ROOT

def ui_checks():
    import tkinter as tk
    from tkinter import ttk
    from hd_emulator import EmulatorWindow
    root=tk.Tk();root.withdraw();args=argparse.Namespace(config=OUT/'actions_settings.json',save_root=OUT/'actions_saves',no_start=True,demo=False,rom=None,state=None,state_frame=64700,paused=False)
    app=EmulatorWindow(root,args);sent=[];app.send=lambda op,**data:sent.append(dict(op=op,**data))
    def key(name):return SimpleNamespace(keysym=name,state=0)
    def descendants(widget):
        for child in widget.winfo_children():yield child;yield from descendants(child)
    try:
        app.settings['hotkeys']['quick_save']='F5';app.loaded=True;app.paused=False
        app.key_down(key('F5'));app.key_down(key('F5'));assert sum(m['op']=='save' for m in sent)==1
        app.key_up(key('F5'));app.key_down(key('F5'));app.key_up(key('F5'));assert sum(m['op']=='save' for m in sent)==2
        app.key_down(key('space'));app.key_down(key('space'));assert app.paused
        app.key_up(key('space'));app.key_down(key('space'));app.key_up(key('space'));assert not app.paused
        app.key_down(key('Pause'));app.key_up(key('Pause'));assert app.paused
        app.key_down(key('F6'));app.key_up(key('F6'));assert not app.paused
        app.key_down(key('Tab'));assert app.fast_forward
        app.key_up(key('Tab'));assert not app.fast_forward and sent[-1]==dict(op='speed',value=1)
        app.key_down(key('Tab'));before=len(sent);app.focus_lost(None)
        assert not app.paused and not app.fast_forward and not app.action_keys_down
        assert not any(m['op']=='pause' for m in sent[before:])
        app.loaded=False;app.shortcuts_dialog();app.dialog.withdraw()
        app.begin_shortcut_capture('shortcut_key','quick_save');app.assign_capture('z');assert app.capture
        app.capture_shortcut_key(key('F7'));assert app.capture is None
        app.begin_shortcut_capture('shortcut_pad','fast_forward');app.assign_capture(9)
        next(w for w in descendants(app.dialog) if isinstance(w,ttk.Button) and w.cget('text')=='적용').invoke()
        stored=read_settings(args.config);assert stored['hotkeys']['quick_save']=='F7' and stored['pad_hotkeys']['fast_forward']==9
        assert not stored['auto_pause']
        app.loaded=True;before=len(sent);app.key_down(key('F7'));app.key_up(key('F7'));assert sent[before]['op']=='save'
        # Both displays must take exactly the same sampling path.
        a=np.zeros((192,256,3),dtype='uint8');a[:,::3]=255;a[::5]=[30,80,190]
        native=Image.fromarray(a);top=native.resize((1440,1080),Image.Resampling.NEAREST)
        app.memory=SimpleNamespace(buf=bytearray(top.tobytes()+top.tobytes()));app.lock=threading.Lock()
        app.receive(dict(event='frame',sequence=1,frame=1));assert app.latest[0].size==app.latest[1].size==(1440,1080)
        assert np.array_equal(np.asarray(app.latest[0]),np.asarray(app.latest[1]))
        for size in ((1707,1280),(936,702),(320,240)):
            assert app.latest[0].resize(size,Image.Resampling.LANCZOS).tobytes()==app.latest[1].resize(size,Image.Resampling.LANCZOS).tobytes()
        app.memory=None
        for mode,size in (('large_horizontal',(1280,720)),('equal_horizontal',(1600,600)),('large_vertical',(960,960)),('equal_vertical',(640,960))):
            rects=screen_rectangles(*size,mode);assert min(r[0] for r in rects)==min(r[1] for r in rects)==0
            assert max(r[0]+r[2] for r in rects)==size[0] and max(r[1]+r[3] for r in rects)==size[1]
        return dict(key_repeat_safe=True,hold_fast_forward=True,pause_resume=True,explicit_pause_resume=True,focus_continues_play=True,key_and_pad_bindings_persist=True,game_input_conflict_rejected=True,screen_sampling_identical=True,fixed_outer_border_removed=True)
    finally:app.memory=None;app.close()

def worker_checks():
    session=Session();session.until('loaded');session.until('frame')
    def measure(speed):
        session.send('speed',value=speed);session.until('speed');session.send('pause',value=True)
        start=session.until('paused')['frame'];session.send('pause',value=False);session.until('paused');time.sleep(1.4)
        session.send('pause',value=True);end=session.until('paused')['frame'];return end-start
    try:
        normal=measure(1);fast=measure(4);restored=measure(1)
        assert fast>normal*1.7,(normal,fast,restored)
        assert .65<restored/max(1,normal)<1.5,(normal,fast,restored)
        session.send('speed',value=999);assert session.until('speed')['value']==1
        return dict(normal_frames=normal,fast_frames=fast,restored_frames=restored,fast_forward_ratio=round(fast/max(1,normal),2),normal_speed_restored=True)
    finally:session.close()

if __name__=='__main__':
    OUT.mkdir(parents=True,exist_ok=True);report=dict(ui=ui_checks(),worker=worker_checks());(OUT/'actions_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
