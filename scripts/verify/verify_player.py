"""Exercise player controls, isolated sessions, save/load and native UI flows.

All preferences, saves and screenshots are confined to test_current/gui.
The two existing ROMs are opened read-only; no test ROM copies are created.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import argparse,json,time,multiprocessing as mp,traceback
from multiprocessing import shared_memory
from types import SimpleNamespace
import numpy as np
from player_controls import *
from player_worker import worker_main,FRAME_BYTES,TOP_BYTES

HERE=(PROJECT_ROOT/'emulator');ROOT=HERE.parent;OUT=ROOT/'test_current/gui'
CANONICAL=ROOT/'release_battle_v02/SRWW_K_Kazuma_BattleVoice_v02.nds'

def controls_checks():
    assert key_buttons({'z','Up'},DEFAULT_KEYS)=={8,4}
    assert key_buttons(set(),DEFAULT_KEYS)==set()
    assert pad_buttons({0},[-1,0],[(0,1)],DEFAULT_PAD)=={8,6,4}
    assert pad_buttons(set(),[.9,0],[(-1,0)],DEFAULT_PAD)=={6}
    assert pad_buttons(set(),[.1,.1],[],DEFAULT_PAD)==set()
    for layout in tuple(mode for mode,_ in LAYOUTS)+('side','stack','top'):
        for swap in (False,True):
            rects=screen_rectangles(1280,720,layout,swap)
            for rect in rects:
                if rect:
                    x,y,w,h=rect;assert x>=0 and y>=0 and x+w<=1280 and y+h<=720
                    assert abs(w/h-4/3)<.01
            if rects[1]:
                x,y,w,h=rects[1];assert touch_position(x+w/2,y+h/2,rects[1])==(0,0)
                assert touch_position(x+w+1,y,rects[1]) is None
                first,second=(rects[::-1] if swap else rects)
                if layout.startswith('large_') or layout=='side':assert abs(first[2]/second[2]-3)<.04 and abs(first[3]/second[3]-3)<.04
                else:assert abs(first[2]-second[2])<=1 and abs(first[3]-second[3])<=1
    for width,height in ((1280,720),(1279,719),(901,603),(720,1281)):
        for layout,_ in LAYOUTS:
            for swap in (False,True):
                rects=screen_rectangles(width,height,layout,swap);first,second=rects[::-1] if swap else rects
                if layout.endswith('vertical'):assert first[1]+first[3]==second[1],(layout,rects)
                else:assert first[0]+first[2]==second[0],(layout,rects)
                x,y,w,h=rects[1];assert touch_position(x+w/2,y+h/2,rects[1])==(0,0)
    path=OUT/'settings_roundtrip.json';settings=read_settings(path);settings['keys']['a']='k';settings['volume']=35
    write_settings(path,settings);assert read_settings(path)['keys']['a']=='k'
    return dict(keyboard=True,pad_mapping=True,dpad_priority=True,four_screen_layouts=True,large_screen_ratio_3_to_1=True,gapless_screen_edges=True,touch_layouts=True,persistent_settings=True)

class Session:
    def __init__(self,rom=CANONICAL,state=None,state_frame=68000):
        ctx=mp.get_context('spawn');self.memory=shared_memory.SharedMemory(create=True,size=FRAME_BYTES);self.lock=ctx.Lock();self.pipe,child=ctx.Pipe()
        config=dict(rom=str(rom),demo=rom==CANONICAL,state=str(state) if state else None,state_frame=state_frame,paused=True,hd=True,volume=0,save_root=str(OUT/'worker_saves'))
        self.process=ctx.Process(target=worker_main,args=(child,self.memory.name,self.lock,config));self.process.start();child.close();self.events=[]
    def send(self,op,**data):self.pipe.send(dict(op=op,**data))
    def until(self,event,timeout=30):
        end=time.perf_counter()+timeout
        while time.perf_counter()<end:
            if self.pipe.poll(.1):
                message=self.pipe.recv();self.events.append(message)
                if message['event']=='error':raise AssertionError(message)
                if message['event']==event:return message
            if not self.process.is_alive():raise AssertionError(f'worker exit: {self.process.exitcode}')
        raise AssertionError(f'timeout waiting for {event}')
    def image(self):
        with self.lock:
            w,h,_,_=np.frombuffer(self.memory.buf,dtype='uint32',count=4,offset=TOP_BYTES*2)
            assert 768<=w<=960 and h==w*3//4
            return np.frombuffer(bytes(self.memory.buf[:int(w*h*4)]),dtype='uint8').reshape(int(h),int(w),4)[:,:,:3].copy()
    def close(self):
        self.send('quit');self.process.join(5)
        if self.process.is_alive():self.process.terminate();self.process.join();raise AssertionError('worker did not close')
        assert self.process.exitcode==0,self.process.exitcode
        self.process.close();self.pipe.close();self.memory.close();self.memory.unlink()

def worker_checks():
    session=Session(state=ROOT/'test_current/combat/quatre_cutin_full.state')
    try:
        loaded=session.until('loaded');session.until('frame');before=session.image();assert before.max()>0
        session.send('hd',value=False);session.until('hd');session.until('frame');native=session.image()
        session.send('hd',value=True);session.until('hd');session.until('frame')
        # A cold first frame may legitimately retain native art while its HD
        # textures load. Compare the same paused cut-in after it is displayed.
        deadline=time.perf_counter()+30
        while not np.any(session.image()!=native):
            assert time.perf_counter()<deadline,'HD cut-in did not finish loading'
            session.until('frame',timeout=max(.1,deadline-time.perf_counter()))
        session.send('save',slot=1);saved=session.until('saved');path=Path(saved['path']);assert path.exists()
        meta=json.loads(path.with_suffix('.state.json').read_text());assert len(meta['rom_hash'])==64
        session.send('pause',value=False);assert session.until('paused')['value'] is False
        session.until('frame');session.send('pause',value=True);session.until('paused')
        session.send('load',slot=1);assert session.until('state_loaded')['paused'];session.until('frame')
        bad=path.parent/'wrong_game.state';bad.write_bytes(path.read_bytes());bad.with_suffix('.state.json').write_text(json.dumps(dict(rom_hash='0'*64)))
        session.send('load',path=str(bad));error=session.until('command_error');assert '다른 롬' in error['message'];assert session.process.is_alive()
    finally:session.close()
    other=Session(rom=ROOT/'baseline/SRWW_Korean_1.0.8.nds')
    try:other.until('loaded');other.until('frame');assert other.image().max()>0
    finally:other.close()
    return dict(shared_frames=True,hd_toggle=True,save_load=True,pause=True,wrong_rom_state_rejected=True,reopened_other_rom=True)

def gui_checks():
    import tkinter as tk
    from tkinter import ttk
    from hd_emulator import EmulatorWindow
    root=tk.Tk();args=argparse.Namespace(config=OUT/'ui_settings.json',save_root=OUT/'ui_saves',no_start=True,demo=False,rom=None,state=None,state_frame=68000,paused=True)
    app=EmulatorWindow(root,args);phase=0;started=time.perf_counter();error=[];report={};old_pid=None;window_id=root.winfo_id()
    def callback_error(kind,value,trace):
        error.append(''.join(traceback.format_exception(kind,value,trace)));app.close()
    root.report_callback_exception=callback_error
    def descendants(widget):
        for child in widget.winfo_children():yield child;yield from descendants(child)
    def step():
        nonlocal phase,started,old_pid
        try:
            if time.perf_counter()-started>35:raise AssertionError(f'UI phase {phase} timed out')
            if phase==0:
                app.start_session(CANONICAL,True,ROOT/'test_current/parts/result.state',68000,True);phase=1;started=time.perf_counter()
            elif phase==1 and app.loaded and app.latest:
                assert app.play_button.instate(['!disabled'])
                width,height=app.latest[0].size
                assert app.latest[1].size==(width,height) and 768<=width<=960 and width%32==0 and height==width*3//4
                app.controls_dialog();app.begin_capture('key','a');app.assign_capture('k')
                apply=next(w for w in descendants(app.dialog) if isinstance(w,ttk.Button) and w.cget('text')=='적용');apply.invoke()
                assert app.settings['keys']['a']=='k';assert read_settings(args.config)['keys']['a']=='k'
                for mode,_ in LAYOUTS:
                    app.choose_layout(mode);app.draw();assert app.layout_var.get()==mode
                    x,y,w,h=app.rects[1];assert touch_position(x+w/2,y+h/2,app.rects[1])==(0,0)
                app.choose_layout('equal_vertical');app.swap_var.set(True);app.set_layout();phase=2
            elif phase==2:
                app.draw();rect=app.rects[1];x,y,w,h=rect
                assert app.canvas.bind('<Double-Button-1>')
                double=SimpleNamespace(x=x+w/2,y=y+h/2)
                app.double_click(double);assert bool(root.attributes('-fullscreen'))
                assert app.toolbar.winfo_manager()=='' and app.layout_toolbar.winfo_manager()=='' and not root.cget('menu')
                app.double_click(double);assert not bool(root.attributes('-fullscreen'))
                assert app.toolbar.winfo_manager()=='pack' and app.layout_toolbar.winfo_manager()=='pack' and root.cget('menu')
                app.double_click(SimpleNamespace(x=0,y=0));assert not bool(root.attributes('-fullscreen'))
                app.mouse_down(SimpleNamespace(x=x+w/2,y=y+h/2));assert app.touch==(0,0);app.mouse_up(None)
                app.canvas.focus_force();app.key_down(SimpleNamespace(keysym='k',state=0));assert key_buttons(app.held,app.settings['keys'])=={8}
                app.focus_lost(None);assert not app.held
                app.slot_var.set(3);app.set_slot();app.quick_save();phase=3
            elif phase==3 and app.save_dir and (app.save_dir/'slot_3.state').exists():
                app.quick_load();phase=4
            elif phase==4 and app.loaded and not app.demo:
                assert app.paused;old_pid=app.process.pid;app.start_session(ROOT/'baseline/SRWW_Korean_1.0.8.nds');phase=5;started=time.perf_counter()
            elif phase==5 and app.loaded and app.latest:
                assert app.process.pid!=old_pid and root.winfo_id()==window_id
                report.update(native_window=True,controls_dialog=True,key_rebind_persisted=True,four_layout_preset_buttons=True,layout_and_touch=True,double_click_fullscreen_roundtrip=True,fullscreen_hides_menus=True,focus_releases_keys=True,slot_save_load=True,rom_switch_preserves_window=True,detected_gamepads=len(app.devices))
                app.close();return
            root.after(100,step)
        except Exception as exc:error.append(repr(exc));app.close()
    root.after(100,step);root.mainloop()
    assert not error,error
    return report

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    report=dict(controls=controls_checks(),worker=worker_checks(),gui=gui_checks())
    (OUT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(report,ensure_ascii=False))

if __name__=='__main__':mp.freeze_support();main()
