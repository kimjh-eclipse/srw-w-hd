"""Keep decoded assets alive for a whole stage, including LRU spill entries."""
from collections import OrderedDict
import weakref
import os

_caches=[]
_stage=None
MAX_BYTES=max(64,int(os.environ.get('SRWW_STAGE_CACHE_MB','1024')))*1024*1024
_entries=OrderedDict()
_bytes=0

def asset_bytes(value):
    if hasattr(value,'nbytes'):return int(value.nbytes)
    if hasattr(value,'getbands') and hasattr(value,'size'):return value.width*value.height*len(value.getbands())
    if isinstance(value,(tuple,list)):return sum(asset_bytes(v) for v in value)
    return 0

def _forget(cache,key):
    global _bytes
    entry=_entries.pop((id(cache),key),None)
    if entry is not None:_bytes-=entry[1]

def cache_stats():return dict(bytes=_bytes,max_bytes=MAX_BYTES,entries=len(_entries),stage=_stage)

def _released(identity):
    global _bytes
    for key in [key for key in _entries if key[0]==identity]:
        _bytes-=_entries.pop(key)[1]

class StageCache(OrderedDict):
    def __init__(self):
        super().__init__();self.retained={};identity=id(self)
        _caches.append(weakref.ref(self,lambda _,identity=identity:_released(identity)))
    def __setitem__(self,key,value):
        global _bytes
        _forget(self,key);self.retained.pop(key,None);super().__setitem__(key,value)
        size=asset_bytes(value);_entries[id(self),key]=(weakref.ref(self),size);_bytes+=size
        while _bytes>MAX_BYTES and _entries:
            (_,victim),(reference,count)=_entries.popitem(last=False);_bytes-=count
            cache=reference()
            if cache is not None:
                OrderedDict.pop(cache,victim,None);cache.retained.pop(victim,None)
                if getattr(cache,'on_evict',None):cache.on_evict()
    def __contains__(self,key):return super().__contains__(key) or key in self.retained
    def __getitem__(self,key):
        if not super().__contains__(key):
            value=self.retained.pop(key);super().__setitem__(key,value)
        identity=(id(self),key)
        if identity in _entries:_entries.move_to_end(identity)
        return super().__getitem__(key)
    def get(self,key,default=None):return self[key] if key in self else default
    def pop(self,key,default=None):
        _forget(self,key)
        if super().__contains__(key):return super().pop(key)
        return self.retained.pop(key,default)
    def move_to_end(self,key,last=True):
        self[key];super().move_to_end(key,last)
    def popitem(self,last=True):
        key,value=super().popitem(last);self.retained[key]=value
        return key,value
    def clear(self):
        changed=bool(OrderedDict.__len__(self) or self.retained)
        for key in list(OrderedDict.keys(self))+list(self.retained):_forget(self,key)
        super().clear();self.retained.clear()
        if changed and getattr(self,'on_evict',None):self.on_evict()

def begin_stage(key):
    global _stage
    if key is None or key==_stage:return False
    _stage=key
    for reference in _caches:
        cache=reference()
        if cache is not None:cache.clear()
    return True
