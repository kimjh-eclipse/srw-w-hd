"""Exact native visibility-mask acceleration with the original NumPy fallback."""
import ctypes as C
from pathlib import Path
import numpy as np
_api=None

def library():
    global _api
    if _api is None:
        try:
            _api=C.CDLL(str(Path(__file__).with_suffix('.dll')))
            _api.part_visibility.argtypes=[C.c_void_p]*4+[C.c_int]*8+[C.c_uint32,C.c_void_p]
            _api.part_visibility.restype=C.c_int
        except (OSError,AttributeError):_api=False
    return _api

class PartVisibility:
    def __init__(self,layers,owners,bgpriorities,objpriorities,native=True):
        self.layers=np.ascontiguousarray(layers,dtype='uint8');self.owners=np.ascontiguousarray(owners,dtype='uint8')
        self.bg=np.ascontiguousarray(bgpriorities,dtype='uint8');self.obj=np.ascontiguousarray(objpriorities,dtype='uint16')
        self.pointers=(self.layers.ctypes.data,self.owners.ctypes.data,self.bg.ctypes.data,self.obj.ctypes.data)
        self.stride=self.layers.shape[1]
        self.api=library() if native else False
        if self.api is False:
            self.bg_all=self.bg[np.minimum(self.layers,5)];self.obj_all=self.obj[self.owners]
    def mask(self,left,top,right,bottom,priority,kind,item,control):
        shape=(bottom-top,right-left)
        if self.api is not False:
            output=np.empty(shape,dtype='uint8')
            state=self.api.part_visibility(*self.pointers,self.stride,left,top,shape[1],shape[0],priority,kind,item,control,output.ctypes.data)
            return output,state
        layers=self.layers[top:bottom,left:right];owners=self.owners[top:bottom,left:right]
        bgprio=self.bg_all[top:bottom,left:right];prio=self.obj_all[top:bottom,left:right]
        visible=((layers<4)&((bgprio>priority)|((bgprio==priority)&((layers>item) if kind else True))))|(layers==5)
        if control&0xc0==0x40 and control&(1<<(8+item if kind else 12)):
            visible|=(layers<4)&(((control>>layers.astype('uint32'))&1)!=0)
        visible|=(layers==4)&((prio>priority)|((prio==priority)&(owners>=item)&(not kind)))
        return visible.astype('uint8')*255,0 if not visible.any() else 2 if visible.all() else 1
