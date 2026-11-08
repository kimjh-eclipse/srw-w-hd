"""Single-pass exact font color masks; no recognition/appearance changes."""
from pathlib import Path
import ctypes as C
import numpy as np

class NativeFontPixels:
    def __init__(self):
        self.api=C.CDLL(str(Path(__file__).with_suffix('.dll')))
        self.api.font_pixel_masks.argtypes=[C.c_void_p,C.c_int,C.c_int]+[C.c_void_p]*5
        self.api.font_pixel_masks.restype=None
        self.size=None
    def masks(self,native):
        native=np.ascontiguousarray(np.asarray(native)[:,:,:3],dtype='uint8');h,w=native.shape[:2]
        if self.size!=(h,w):
            self.size=(h,w);self.buffers=[np.empty((h,w),dtype='bool') for _ in range(3)]+[np.empty((min(32,h),w),dtype='bool') for _ in range(2)]
        self.api.font_pixel_masks(native.ctypes.data,h,w,*(a.ctypes.data for a in self.buffers))
        return self.buffers
