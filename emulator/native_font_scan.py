"""ctypes bridge for exact bitmap matches, with immutable table registration."""
from pathlib import Path
import ctypes as C
import numpy as np

class NativeFontScanner:
    def __init__(self):
        self.api=C.CDLL(str(Path(__file__).with_suffix('.dll')));self.tables={};self.output=np.empty((256*192,3),dtype='int32')
        self.api.font_table_create.argtypes=[C.c_void_p,C.c_int,C.c_int,C.c_int,C.c_int];self.api.font_table_create.restype=C.c_void_p
        self.api.font_table_free.argtypes=[C.c_void_p];self.api.font_table_free.restype=None
        self.api.font_scan.argtypes=[C.c_void_p,C.c_void_p,C.c_int,C.c_int,C.c_int,C.c_int,C.c_void_p,C.c_int];self.api.font_scan.restype=C.c_int
    def scan(self,mask,height,width,keys,characters,minimum=1,maximum=144):
        identity=(id(keys),height,width)
        if identity not in self.tables:
            packed=np.ascontiguousarray(keys)
            handle=self.api.font_table_create(packed.ctypes.data,len(keys),height,width,keys.dtype.itemsize)
            if not handle:raise MemoryError('Native glyph table registration failed')
            self.tables[identity]=(handle,keys,packed)
        native=np.ascontiguousarray(mask,dtype='uint8');rows,cols=native.shape
        needed=max(1,(rows-height+1)*(cols-width+1))
        if len(self.output)<needed:self.output=np.empty((needed,3),dtype='int32')
        count=self.api.font_scan(self.tables[identity][0],native.ctypes.data,rows,cols,minimum,maximum,self.output.ctypes.data,len(self.output))
        if count<0:raise RuntimeError('Native glyph scan failed: '+str(count))
        return [(int(x),int(y),characters[i],width,height,mask[y:y+height,x:x+width].copy()) for x,y,i in self.output[:count]]
    def close(self):
        for handle,keys,packed in self.tables.values():self.api.font_table_free(handle)
        self.tables.clear()
