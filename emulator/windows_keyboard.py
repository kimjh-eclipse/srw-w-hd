"""Foreground-only physical key sampling for the SDL-embedded Tk canvas.

SDL foreign windows can consume key messages before Tk receives them. Sampling
the configured keys also retains taps shorter than one emulation frame.
"""
import os,time
from types import SimpleNamespace

class WindowsKeyboard:
    def __init__(self):
        self.down=set();self.events=0;self.api=None;self.active=False
        if os.name=='nt':
            import ctypes as C
            self.api=C.windll.user32
            self.api.GetAsyncKeyState.argtypes=[C.c_int];self.api.GetAsyncKeyState.restype=C.c_short

    def virtual_key(self,key):
        aliases=dict(Left=37,Up=38,Right=39,Down=40,space=32,Return=13,Tab=9,Escape=27,Pause=19,BackSpace=8,Shift_L=160,Shift_R=161,Control_L=162,Control_R=163,Alt_L=164,Alt_R=165,Home=36,End=35,Prior=33,Next=34,Insert=45,Delete=46)
        if key in aliases:return aliases[key]
        if key.startswith('F') and key[1:].isdigit():return 111+int(key[1:])
        if key.startswith('KP_') and key[3:].isdigit():return 96+int(key[3:])
        if len(key)==1:
            value=self.api.VkKeyScanW(ord(key))
            return value&255 if value!=-1 else None
        return None

    def poll(self,app):
        if self.api is None:return
        if app.dialog or not app.loaded or not app.has_input_focus():
            self.down.clear();self.active=False;return
        was_active=self.active;self.active=True
        keys=set(app.settings['keys'].values())|set(app.settings['hotkeys'].values())|{'F1','F11','Escape'}
        keys.discard(None);state=(1 if self.api.GetAsyncKeyState(16)&0x8000 else 0)|(4 if self.api.GetAsyncKeyState(17)&0x8000 else 0)|(8 if self.api.GetAsyncKeyState(18)&0x8000 else 0)
        for key in keys:
            code=self.virtual_key(key)
            if code is None:continue
            bits=self.api.GetAsyncKeyState(code)&0xffff;held=bool(bits&0x8000);tap=bool(bits&1)
            down=held and key not in self.down
            if not held and tap and key not in self.down:down=True
            if not was_active:down=False
            if down:
                seen=getattr(app,'tk_key_seen',{}).get((key,True),-10)
                sdl_seen=app.gpu.forwarded_keys.get((key,True),-10) if app.gpu else -10
                if time.perf_counter()-max(seen,sdl_seen)>=.04:
                    event=SimpleNamespace(keysym=key,state=state,from_sdl=True);self.events+=1
                    if key=='F1':app.toggle_hd()
                    elif key=='F11':app.fullscreen()
                    elif key=='Escape':app.leave_fullscreen()
                    else:app.key_down(event)
            if not held and (key in self.down or down):app.key_up(SimpleNamespace(keysym=key,state=state,from_sdl=True))
            if held:self.down.add(key)
            else:self.down.discard(key)
