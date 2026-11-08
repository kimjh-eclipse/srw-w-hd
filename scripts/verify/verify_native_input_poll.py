"""Headless regression tests for native pointer/keyboard and safe SDL pad polling.

No Tk/SDL windows are constructed. event.get is forbidden throughout.
"""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

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
    """Exercise the isolated native worker without opening a Tk window."""
    from scripts.verify.verify_pad_process import run_headless
    return run_headless()


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(NativeInputTests))
    report={'pointer_keyboard_tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors)}
    if result.wasSuccessful():report['headless_hotplug']=verify_headless_hotplug()
    output=PROJECT_ROOT/'test_current/gui/native_input_poll_verification.json'
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report));raise SystemExit(0 if result.wasSuccessful() else 1)
