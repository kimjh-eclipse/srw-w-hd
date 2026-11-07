"""Headless regression tests for native pointer/keyboard and safe SDL pad polling.

No Tk/SDL windows are constructed. event.get is forbidden throughout.
"""
import copy
import ctypes as C
from ctypes import wintypes
import json
import os
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import Mock, patch

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from gpu_display import GPUDisplay
from windows_keyboard import WindowsKeyboard


class NativeAPI:
    def __init__(self):
        self.bits = {}; self.x = 30; self.y = 40
    def GetAsyncKeyState(self, code):
        value = self.bits.get(code, 0)
        self.bits[code] = value & 0x8000
        return value
    def GetCursorPos(self, point):
        point._obj.x = self.x; point._obj.y = self.y
    def ScreenToClient(self, handle, point): pass
    def GetDoubleClickTime(self): return 500
    def VkKeyScanW(self, char): return ord(chr(char).upper())


class InputApp:
    def __init__(self):
        self.dialog = None; self.loaded = True; self.focus = True
        self.canvas = NS(winfo_width=lambda: 320, winfo_height=lambda: 240)
        self.settings = {'keys': {'a': 'z'}, 'hotkeys': {'pause': 'space'}}
        self.gpu = NS(forwarded_keys={}); self.tk_key_seen = {}; self.tk_pointer_seen = None
        self.calls = []
    def has_input_focus(self): return self.focus
    def mouse_down(self, e): self.calls.append(('down', e.x, e.y))
    def mouse_up(self, e): self.calls.append(('up', getattr(e, 'x', None), getattr(e, 'y', None)))
    def mouse_drag(self, e): self.calls.append(('drag', e.x, e.y))
    def double_click(self, e): self.calls.append(('fullscreen', e.x, e.y))
    def key_down(self, e): self.calls.append(('key_down', e.keysym, e.state))
    def key_up(self, e): self.calls.append(('key_up', e.keysym, e.state))
    def toggle_hd(self): self.calls.append(('hd',))
    def fullscreen(self): self.calls.append(('fullscreen',))
    def leave_fullscreen(self): self.calls.append(('leave_fullscreen',))


class NativeInputTests(unittest.TestCase):
    def setUp(self):
        self.api = NativeAPI(); self.app = InputApp(); self.now = 100.
        self.clock = patch('time.perf_counter', side_effect=lambda: self.now); self.clock.start()
        self.addCleanup(self.clock.stop)
        self.gpu = GPUDisplay.__new__(GPUDisplay)
        self.gpu.canvas_id = 1; self.gpu.pointer_api = self.api; self.gpu.pointer_point = wintypes.POINT()
        self.gpu.pointer_down = False; self.gpu.pointer_tracking = False
        self.gpu.pointer_last = None; self.gpu.pointer_click = None; self.gpu.mouse_events = 0
        self.gpu.focused = lambda: self.app.focus
        self.keyboard = WindowsKeyboard.__new__(WindowsKeyboard)
        self.keyboard.api = self.api; self.keyboard.down = set(); self.keyboard.active = False; self.keyboard.events = 0
    def pointer(self, held, x=None, y=None):
        self.now += .01; self.api.bits[1] = 0x8000 if held else 0
        if x is not None: self.api.x = x
        if y is not None: self.api.y = y
        self.gpu.events(self.app)
    def key(self, bits, code=90):
        self.now += .01; self.api.bits[code] = bits; self.keyboard.poll(self.app)
    def test_click_drag_release(self):
        self.pointer(True); self.pointer(True); self.pointer(True, 55, 65)
        self.pointer(False); self.pointer(False)
        self.assertEqual(self.app.calls, [('down',30,40),('drag',55,65),('up',55,65)])
    def test_native_foreground_matches_root_ancestor(self):
        api=NS(GetForegroundWindow=Mock(return_value=7),GetAncestor=Mock(return_value=7))
        with patch.object(C.windll,'user32',api):
            self.assertTrue(GPUDisplay.focused(self.gpu))
            api.GetAncestor.assert_called_with(1,2)
            api.GetForegroundWindow.return_value=8
            self.assertFalse(GPUDisplay.focused(self.gpu))
    def test_double_click_toggles_once_per_pair(self):
        for _ in range(2):
            self.pointer(True); self.pointer(False); self.pointer(True); self.pointer(True); self.pointer(False)
        self.assertEqual(sum(c[0]=='fullscreen' for c in self.app.calls), 2)
        self.assertEqual(sum(c[0]=='down' for c in self.app.calls), 2)
    def test_tk_pointer_duplicates_are_suppressed(self):
        self.app.tk_pointer_seen = ('down',30,40,self.now); self.pointer(True)
        self.app.tk_pointer_seen = ('up',30,40,self.now); self.pointer(False)
        self.assertEqual(self.app.calls, [])
    def test_focus_loss_releases_drag_and_ignores_outside(self):
        self.pointer(True); self.app.focus=False; self.pointer(True); self.pointer(False)
        self.app.focus=True; self.pointer(False); self.pointer(True, -1,40)
        self.assertEqual(self.app.calls,[('down',30,40),('up',None,None)])
    def test_dialog_and_unloaded_ignore_pointer(self):
        self.app.dialog=True; self.pointer(True); self.pointer(False)
        self.app.dialog=None; self.app.loaded=False; self.pointer(True); self.pointer(False)
        self.assertEqual(self.app.calls,[])
    def test_short_tap_delivers_press_and_release(self):
        self.key(0); self.key(1)
        self.assertEqual(self.app.calls,[('key_down','z',0),('key_up','z',0)])
    def test_initial_stale_tap_is_discarded(self):
        self.key(1); self.key(0)
        self.assertEqual(self.app.calls,[])
    def test_focus_entry_with_held_key_does_not_fire_shortcut(self):
        self.key(0x8001)
        for _ in range(3):self.key(0x8000)
        self.assertFalse(any(c[0]=='key_down' for c in self.app.calls))
        self.key(0);self.app.calls.clear();self.key(0x8001);self.key(0)
        self.assertEqual(self.app.calls,[('key_down','z',0),('key_up','z',0)])
    def test_held_key_has_one_press_one_release(self):
        self.key(0); self.key(0x8001)
        for _ in range(10): self.key(0x8001)
        self.key(0)
        self.assertEqual(self.app.calls,[('key_down','z',0),('key_up','z',0)])
    def test_tk_key_duplicate_and_foreground_gate(self):
        self.key(0); self.app.tk_key_seen[('z',True)] = self.now; self.key(1)
        self.assertFalse(any(c[0]=='key_down' for c in self.app.calls))
        self.app.calls.clear(); self.app.focus=False; self.key(1)
        self.assertEqual(self.app.calls,[])
        self.app.focus=True; self.key(1); self.key(0)
        self.assertEqual(self.app.calls,[])
    def test_special_shortcuts_and_modifier_state(self):
        self.key(0); self.api.bits[16]=0x8000; self.key(1,112)
        self.key(1,122); self.key(1,27); self.key(1)
        self.assertEqual([c for c in self.app.calls if c[0] not in ('key_down','key_up')],[('hd',),('fullscreen',),('leave_fullscreen',)])
        self.assertEqual(self.app.calls[-2:], [('key_down','z',1),('key_up','z',1)])


def verify_headless_hotplug():
    """Same native scenarios as verify_pad_hotplug, without its Tk/get prelude."""
    import pygame
    from hd_emulator import EmulatorWindow
    from player_controls import DEFAULTS
    pygame.display.init(); pygame.joystick.init()
    app=EmulatorWindow.__new__(EmulatorWindow)
    app.pygame=pygame; app.settings=copy.deepcopy(DEFAULTS)
    app.dialog=None; app.loaded=True; app.pad=None; app.devices=[]; app.capture=None; app.pad_draft=None
    app.pad_status=NS(set=lambda text:None); app.rumble=NS(stop=lambda:None)
    app.persist=lambda:None; app.has_input_focus=lambda:True
    app.controller_defaults=lambda:dict(app.settings['pad'])
    app.last_device_refresh=0; app.pad_button_snapshot=(None,set())
    commands=[]; app.run_action=commands.append
    app.settings['pad_hotkeys'].update(fast_forward=8,quick_save=9,quick_load=10,pause_resume=11)
    sdl=C.CDLL(str(Path(pygame.__file__).parent/'SDL2.dll'))
    class Event(C.Structure):
        _fields_=[('type',C.c_uint32),('timestamp',C.c_uint32),('which',C.c_int32),('padding',C.c_ubyte*44)]
    signatures={'SDL_PushEvent':([C.POINTER(Event)],C.c_int),'SDL_JoystickAttachVirtual':([C.c_int,C.c_int,C.c_int,C.c_int],C.c_int),'SDL_JoystickDetachVirtual':([C.c_int],C.c_int),'SDL_JoystickOpen':([C.c_int],C.c_void_p),'SDL_JoystickClose':([C.c_void_p],None),'SDL_JoystickSetVirtualButton':([C.c_void_p,C.c_int,C.c_ubyte],C.c_int)}
    for name,(args,result) in signatures.items():
        fn=getattr(sdl,name);fn.argtypes=args;fn.restype=result
    with patch.object(pygame.event,'get',side_effect=AssertionError('unsafe event.get called')):
        for _ in range(20):
            assert sdl.SDL_PushEvent(C.byref(Event(type=pygame.JOYDEVICEREMOVED,which=2147483000)))==1
            assert isinstance(app.poll_pad(),set)
        for _ in range(3):
            index=sdl.SDL_JoystickAttachVirtual(1,2,12,1); assert index>=0
            handle=sdl.SDL_JoystickOpen(index); assert handle
            try:
                app.refresh_devices();app.pad=pygame.joystick.Joystick(index);app.poll_pad()
                captured=[];app.capture=('pad','a');app.assign_capture=captured.append
                assert sdl.SDL_JoystickSetVirtualButton(handle,0,1)==0
                assert 8 in app.poll_pad();app.poll_pad();assert captured==[0]
                sdl.SDL_JoystickSetVirtualButton(handle,0,0);app.poll_pad();app.capture=None
                for button,action in [(8,'fast_forward'),(9,'quick_save'),(10,'quick_load'),(11,'pause_resume')]:
                    before=commands.count(action);sdl.SDL_JoystickSetVirtualButton(handle,button,1)
                    app.poll_pad();app.poll_pad();assert commands.count(action)==before+1
                    if button==8:assert app.pad_fast_forward
                    sdl.SDL_JoystickSetVirtualButton(handle,button,0);app.poll_pad()
                    if button==8:assert not app.pad_fast_forward
            finally:
                sdl.SDL_JoystickClose(handle);sdl.SDL_JoystickDetachVirtual(index)
            app.poll_pad();assert app.pad is None or app.pad.get_init()
        with patch.object(pygame.event,'pump',side_effect=SystemError('simulated native failure')):
            assert app.poll_pad()==set();assert app.pad is None
    return {'stale_native_events':20,'virtual_attach_capture_hotkey_detach_cycles':3,'unsafe_event_get_calls':0,'native_error_recovery':True}


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeInputTests))
    report={'pointer_keyboard_tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}
    if result.wasSuccessful():report['headless_hotplug']=verify_headless_hotplug()
    output=Path(__file__).resolve().parent.parent/'test_current/gui/native_input_poll_verification.json'
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report));raise SystemExit(0 if result.wasSuccessful() else 1)
