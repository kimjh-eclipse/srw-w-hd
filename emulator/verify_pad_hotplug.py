"""Reproduce stale native SDL events and verify Tk input keeps running."""
from pathlib import Path
import os,json,ctypes as C,argparse
os.environ['PYGAME_HIDE_SUPPORT_PROMPT']='1'
import pygame
import tkinter as tk
from hd_emulator import EmulatorWindow,ROOT
OUT=ROOT/'test_current/gui';OUT.mkdir(parents=True,exist_ok=True)
sdl=C.CDLL(str(Path(pygame.__file__).parent/'SDL2.dll'))
class Event(C.Structure):_fields_=[('type',C.c_uint32),('timestamp',C.c_uint32),('which',C.c_int32),('padding',C.c_ubyte*44)]
sdl.SDL_PushEvent.argtypes=[C.POINTER(Event)];sdl.SDL_PushEvent.restype=C.c_int
def stale():
    event=Event(type=pygame.JOYDEVICEREMOVED,which=2147483000)
    assert sdl.SDL_PushEvent(C.byref(event))==1
pygame.display.init();pygame.joystick.init();pygame.event.clear()
stale();old_error=None
try:pygame.event.get()
except (SystemError,KeyError) as exc:old_error=type(exc).__name__+': '+str(exc)
assert old_error,'Original stale-event crash was not reproduced'
args=argparse.Namespace(config=OUT/'hotplug_settings.json',save_root=OUT/'hotplug_saves',no_start=True,demo=False,rom=None,state=None,state_frame=64700,paused=True)
root=tk.Tk();root.withdraw();app=EmulatorWindow(root,args);results={}
try:
    for _ in range(20):stale();assert isinstance(app.poll_pad(),set)
    results['native_stale_events_survived']=20
    sdl.SDL_JoystickAttachVirtual.argtypes=[C.c_int,C.c_int,C.c_int,C.c_int];sdl.SDL_JoystickAttachVirtual.restype=C.c_int
    sdl.SDL_JoystickDetachVirtual.argtypes=[C.c_int];sdl.SDL_JoystickDetachVirtual.restype=C.c_int
    sdl.SDL_JoystickOpen.argtypes=[C.c_int];sdl.SDL_JoystickOpen.restype=C.c_void_p
    sdl.SDL_JoystickClose.argtypes=[C.c_void_p]
    sdl.SDL_JoystickSetVirtualButton.argtypes=[C.c_void_p,C.c_int,C.c_ubyte];sdl.SDL_JoystickSetVirtualButton.restype=C.c_int
    commands=[];app.send=lambda op,**data:commands.append(dict(op=op,**data));app.loaded=True;app.paused=False
    app.root.focus_displayof=lambda:app.canvas
    app.settings['pad_hotkeys'].update(fast_forward=8,quick_save=9,quick_load=10,pause_resume=11)
    for _ in range(3):
        index=sdl.SDL_JoystickAttachVirtual(1,2,12,1);assert index>=0
        handle=None
        try:
            app.refresh_devices();virtual=pygame.joystick.Joystick(index);app.pad=virtual;app.poll_pad()
            handle=sdl.SDL_JoystickOpen(index);assert handle
            captured=[];original=app.assign_capture;app.assign_capture=captured.append;app.capture=('pad','a')
            assert sdl.SDL_JoystickSetVirtualButton(handle,0,1)==0
            assert 8 in app.poll_pad();assert captured==[0]
            app.poll_pad();assert captured==[0],'Held button was captured repeatedly'
            assert sdl.SDL_JoystickSetVirtualButton(handle,0,0)==0
            assert 8 not in app.poll_pad()
            app.assign_capture=original;app.capture=None
            assert sdl.SDL_JoystickSetVirtualButton(handle,8,1)==0
            app.poll_pad();assert app.pad_fast_forward;app.set_fast_forward(app.pad_fast_forward);assert app.fast_forward
            assert sdl.SDL_JoystickSetVirtualButton(handle,8,0)==0
            app.poll_pad();app.set_fast_forward(app.pad_fast_forward);assert not app.fast_forward
            for button,op in ((9,'save'),(10,'load')):
                before=sum(m['op']==op for m in commands)
                assert sdl.SDL_JoystickSetVirtualButton(handle,button,1)==0
                app.poll_pad();app.poll_pad();assert sum(m['op']==op for m in commands)==before+1
                assert sdl.SDL_JoystickSetVirtualButton(handle,button,0)==0
                app.poll_pad()
            assert sdl.SDL_JoystickSetVirtualButton(handle,11,1)==0
            app.poll_pad();app.poll_pad();assert app.paused
            assert sdl.SDL_JoystickSetVirtualButton(handle,11,0)==0
            app.poll_pad()
            assert sdl.SDL_JoystickSetVirtualButton(handle,11,1)==0
            app.poll_pad();assert not app.paused
            assert sdl.SDL_JoystickSetVirtualButton(handle,11,0)==0
            app.poll_pad()
        finally:
            if handle:sdl.SDL_JoystickClose(handle)
            assert sdl.SDL_JoystickDetachVirtual(index)==0
        app.poll_pad();assert app.pad is None or app.pad.get_init()
    results['virtual_attach_input_capture_detach_cycles']=3
    results['controller_fast_forward_save_load_pause_resume']=True
    import sdl_pad_state
    original_update=sdl_pad_state.update
    def fail():raise SystemError('simulated device failure')
    sdl_pad_state.update=lambda pygame:fail()
    try:assert app.poll_pad()==set()
    finally:sdl_pad_state.update=original_update
    results['system_error_releases_pad_and_rumble']=app.pad is None
    # Exercise the actual Tk callback after the native stale-event failure:
    # another timer must run and the keyboard binding must still be usable.
    stale();app.held.add('z');app.poll();root.update()
    assert 'z' in app.held
    results['tk_poll_and_keyboard_continue']=True
finally:app.close()
report=dict(original_error=old_error,checks=results)
(OUT/'hotplug_verification.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
