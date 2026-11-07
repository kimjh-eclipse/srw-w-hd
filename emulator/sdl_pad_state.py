"""Refresh controller state without dispatching native Tk window messages."""
import ctypes
from pathlib import Path

_library=None

def update(pygame):
    global _library
    if _library is None:
        _library=ctypes.PyDLL(str(Path(pygame.__file__).parent/'SDL2.dll'))
        _library.SDL_JoystickUpdate.argtypes=[]
        _library.SDL_JoystickUpdate.restype=None
        _library.SDL_FlushEvents.argtypes=[ctypes.c_uint32,ctypes.c_uint32]
        _library.SDL_FlushEvents.restype=None
    _library.SDL_JoystickUpdate()
    _library.SDL_FlushEvents(0,0xffff)
