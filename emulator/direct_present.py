"""A GL child window of the UI canvas, owned by the composing process.

Composition and display then share one OpenGL context: a finished frame is
drawn to the screen without being read back, copied through shared memory and
uploaded again by the UI process.
"""
import ctypes as C
from ctypes import wintypes as W


class _PixelFormat(C.Structure):
    _fields_=[('nSize',W.WORD),('nVersion',W.WORD),('dwFlags',W.DWORD),('iPixelType',C.c_byte),('cColorBits',C.c_byte),('pad',C.c_byte*13),
              ('cDepthBits',C.c_byte),('cStencilBits',C.c_byte),('cAuxBuffers',C.c_byte),('iLayerType',C.c_byte),('bReserved',C.c_byte),
              ('dwLayerMask',W.DWORD),('dwVisibleMask',W.DWORD),('dwDamageMask',W.DWORD)]


class PresentWindow:
    def __init__(self,parent):
        user=self.user=C.WinDLL('user32',use_last_error=True);gdi=self.gdi=C.WinDLL('gdi32',use_last_error=True);gl=self.gl=C.WinDLL('opengl32',use_last_error=True)
        user.CreateWindowExW.restype=W.HWND;user.CreateWindowExW.argtypes=[W.DWORD,W.LPCWSTR,W.LPCWSTR,W.DWORD,C.c_int,C.c_int,C.c_int,C.c_int,W.HWND,W.HMENU,W.HINSTANCE,W.LPVOID]
        user.GetDC.restype=W.HDC;user.GetDC.argtypes=[W.HWND];user.GetClientRect.argtypes=[W.HWND,C.POINTER(W.RECT)]
        user.SetWindowPos.argtypes=[W.HWND,W.HWND,C.c_int,C.c_int,C.c_int,C.c_int,C.c_uint];user.ShowWindow.argtypes=[W.HWND,C.c_int]
        user.IsWindow.argtypes=[W.HWND];user.DestroyWindow.argtypes=[W.HWND]
        gdi.ChoosePixelFormat.argtypes=[W.HDC,C.POINTER(_PixelFormat)];gdi.SetPixelFormat.argtypes=[W.HDC,C.c_int,C.POINTER(_PixelFormat)];gdi.SwapBuffers.argtypes=[W.HDC]
        gl.wglCreateContext.restype=W.HANDLE;gl.wglCreateContext.argtypes=[W.HDC];gl.wglMakeCurrent.argtypes=[W.HDC,W.HANDLE]
        gl.wglGetProcAddress.restype=C.c_void_p;gl.wglGetProcAddress.argtypes=[C.c_char_p]
        self.parent=parent;self.size=(0,0);self.visible=False
        if not user.IsWindow(parent):raise OSError('The game canvas is not available')
        # Child, initially hidden, disabled: pointer and keyboard input keep
        # going to the UI canvas underneath.
        self.hwnd=user.CreateWindowExW(0,'STATIC','',0x40000000|0x08000000,0,0,16,16,parent,None,None,None)
        if not self.hwnd:raise OSError(C.get_last_error(),'CreateWindowEx')
        self.dc=user.GetDC(self.hwnd);pixel=_PixelFormat();pixel.nSize=C.sizeof(_PixelFormat);pixel.nVersion=1;pixel.dwFlags=0x4|0x20|0x1;pixel.cColorBits=32
        chosen=gdi.ChoosePixelFormat(self.dc,C.byref(pixel))
        if not chosen or not gdi.SetPixelFormat(self.dc,chosen,C.byref(pixel)):raise OSError(C.get_last_error(),'pixel format')
        self.context=gl.wglCreateContext(self.dc)
        if not self.context or not gl.wglMakeCurrent(self.dc,self.context):raise OSError(C.get_last_error(),'OpenGL context')
        # Frame pacing belongs to the emulator, not to the monitor refresh.
        address=gl.wglGetProcAddress(b'wglSwapIntervalEXT')
        if address:C.WINFUNCTYPE(C.c_int,C.c_int)(address)(0)

    def fit(self):
        """Cover the canvas. Sizes are read here: the UI process may use a
        different DPI scale than this one."""
        rect=W.RECT()
        if not self.user.GetClientRect(self.parent,C.byref(rect)):return None
        size=(max(1,rect.right),max(1,rect.bottom))
        if size!=self.size:
            self.user.SetWindowPos(self.hwnd,None,0,0,size[0],size[1],0x0004|0x0010);self.size=size
        return size

    def show(self):
        if not self.visible:self.user.ShowWindow(self.hwnd,4);self.visible=True   # SW_SHOWNOACTIVATE

    def swap(self):self.gdi.SwapBuffers(self.dc)

    def alive(self):return bool(self.user.IsWindow(self.parent)) and bool(self.user.IsWindow(self.hwnd))

    def pump(self):
        message=W.MSG()
        while self.user.PeekMessageW(C.byref(message),None,0,0,1):
            self.user.TranslateMessage(C.byref(message));self.user.DispatchMessageW(C.byref(message))
