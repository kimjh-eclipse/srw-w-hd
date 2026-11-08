"""Native virtual hotplug, held-button release and helper-crash isolation."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time,os
from pathlib import Path
from pad_process import PadClient

ROOT=PROJECT_ROOT

def wait(client,predicate,ui=None,timeout=7):
    end=time.perf_counter()+timeout
    while time.perf_counter()<end:
        client.poll()
        if ui:ui()
        if predicate():return
        time.sleep(.005)
    raise AssertionError('Timed out waiting for controller state')

def command(client,op,ui=None,**data):
    token=time.perf_counter_ns();assert client.send('test_'+op,id=token,**data)
    wait(client,lambda:client.test_result.get('id')==token,ui)
    result=dict(client.test_result)
    if op=='attach':assert 'instance' in result,(op,token,result,client.epoch,client.restarts)
    return result

def run_headless():
    from player_rumble import PadRumble
    client=PadClient(testing=True);parent=os.getpid();rumble=PadRumble();report={}
    try:
        wait(client,lambda:bool(client.test_result) or client.last_update>client.started)
        report['physical_devices_detected']=[d.get_name() for d in client.devices()]
        for _ in range(12):
            instance=command(client,'attach')['instance'];wait(client,lambda:instance in client.states)
            pad=next(p for p in client.devices() if p.instance==instance)
            command(client,'button',button=0,value=1);wait(client,lambda:pad.get_button(0))
            command(client,'axis',axis=0,value=20000);wait(client,lambda:pad.get_axis(0)>.5)
            rumble.play(pad,True,100,low=1,high=1,duration=50);rumble.stop()
            command(client,'detach');wait(client,lambda:not pad.get_init())
            assert not pad.rumble(1,1,50),'Detached pad accepted rumble'
        report['virtual_attach_input_rumble_detach_cycles']=12
        instance=command(client,'attach')['instance'];wait(client,lambda:instance in client.states)
        old=next(p for p in client.devices() if p.instance==instance);epoch=client.epoch
        command(client,'button',button=0,value=1);wait(client,lambda:old.get_button(0))
        assert client.send('test_crash');wait(client,lambda:not old.get_init())
        wait(client,lambda:client.epoch>epoch and client.process is not None and client.process.is_alive() and client.last_update>client.started)
        assert os.getpid()==parent;report['native_helper_crash_survived_and_restarted']=True
        instance=command(client,'attach')['instance'];wait(client,lambda:instance in client.states)
        epoch=client.epoch;assert client.send('test_hang')
        wait(client,lambda:not client.states,timeout=1)
        wait(client,lambda:client.epoch>epoch and client.process is not None and client.process.is_alive() and client.last_update>client.started,timeout=8)
        report['hung_helper_released_input_and_restarted']=True
    finally:client.close()
    report['clean_shutdown']=client.process is None
    return report

def run_gui():
    import tkinter as tk
    from types import SimpleNamespace
    from unittest.mock import patch
    from hd_emulator import EmulatorWindow
    from gpu_display import RGBFrame
    from PIL import Image
    root=tk.Tk();out=ROOT/'test_current/gui'
    args=SimpleNamespace(config=out/'isolated_pad_settings.json',save_root=out/'isolated_pad_saves',no_start=True,demo=False,rom=None,state=None,state_frame=64700,paused=True)
    with patch('hd_emulator.PadClient',lambda:PadClient(testing=True)):app=EmulatorWindow(root,args)
    client=app.pad_client;errors=[];root.report_callback_exception=lambda *exc:errors.append(str(exc[1]));heartbeats=[]
    pixels=Image.new('RGBA',(768,576),(12,55,91)).tobytes();app.latest=(RGBFrame(pixels,(768,576)),RGBFrame(pixels,(768,576)));app.loaded=True
    app.has_input_focus=lambda:True;commands=[];app.send=lambda op,**data:commands.append(dict(op=op,**data))
    app.settings['pad_hotkeys'].update(fast_forward=8,quick_save=9,quick_load=10,pause_resume=11)
    def heartbeat():
        if app.closed:return
        heartbeats.append(time.perf_counter());app.dirty=True;root.after(16,heartbeat)
    root.after(1,heartbeat)
    try:
        wait(client,lambda:client.last_update>client.started,root.update)
        for _ in range(8):
            instance=command(client,'attach',root.update)['instance'];wait(client,lambda:instance in client.states,root.update)
            app.settings['pad_name']=client.states[instance]['name'];app.refresh_devices();assert app.pad
            command(client,'button',root.update,button=0,value=1)
            wait(client,lambda:8 in app.poll_pad(),root.update)
            command(client,'button',root.update,button=0,value=0);wait(client,lambda:8 not in app.poll_pad(),root.update)
            for button,op in ((9,'save'),(10,'load')):
                before=sum(m['op']==op for m in commands);command(client,'button',root.update,button=button,value=1)
                try:wait(client,lambda:sum(m['op']==op for m in commands)==before+1,root.update)
                except AssertionError:
                    raise AssertionError(dict(button=button,op=op,before=before,commands=commands[-10:],pad=app.pad.get_name() if app.pad else None,buttons=app.pad.state()['buttons'] if app.pad else None,previous=app.pad_button_snapshot,loaded=app.loaded,errors=errors,hotkeys=app.settings['pad_hotkeys']))
                for _ in range(5):app.poll_pad()
                assert sum(m['op']==op for m in commands)==before+1
                command(client,'button',root.update,button=button,value=0)
            command(client,'button',root.update,button=8,value=1);wait(client,lambda:app.pad_fast_forward,root.update)
            command(client,'button',root.update,button=8,value=0);wait(client,lambda:not app.pad_fast_forward,root.update)
            was_paused=app.paused;command(client,'button',root.update,button=11,value=1)
            wait(client,lambda:app.paused!=was_paused,root.update)
            for _ in range(5):app.poll_pad()
            assert app.paused!=was_paused
            command(client,'button',root.update,button=11,value=0)
            app.rumble.play(app.pad,True,100,low=1,high=1,duration=50);command(client,'detach',root.update)
            wait(client,lambda:not app.poll_pad(),root.update);assert not app.last_pad_buttons
        old_epoch=client.epoch;before=len(heartbeats);assert client.send('test_crash')
        wait(client,lambda:client.epoch>old_epoch and client.process is not None and client.process.is_alive() and client.last_update>client.started,root.update)
        assert len(heartbeats)>before+10 and not errors
        assert not app.pygame.joystick.get_init(),'The Tk process initialized native joystick APIs'
        assert app.gpu is not None and app.gpu.presented>10,'GPU display did not keep presenting'
        app.held.add('z');app.flush_game_input();assert commands[-1]['buttons']==[8]
        return dict(gpu_hotplug_cycles=8,gui_frames=app.gpu.presented,ui_heartbeat_after_helper_crash=True,keyboard_after_helper_crash=True,tk_joystick_subsystem_uninitialized=True,save_load_shortcuts_once_per_press=True,fast_forward_and_pause_shortcuts=True,ui_errors=errors)
    finally:
        app.close();args.config.unlink(missing_ok=True)

def main():
    result=dict(headless=run_headless(),gui=run_gui());out=ROOT/'test_current/gui/isolated_pad_verification.json';out.write_text(json.dumps(result,indent=2));print(json.dumps(result))

if __name__=='__main__':main()
