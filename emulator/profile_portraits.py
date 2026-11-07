"""Measure two portrait renderers without launching or modifying the game."""
import ctypes as C,json,time,statistics,threading
from pathlib import Path
from unittest.mock import patch
import numpy as np
from PIL import Image
from hd_portraits import PortraitRenderer
ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'test_current/portrait'
class Memory(C.Structure):
    _fields_=[('cb',C.c_ulong),('faults',C.c_ulong)]+[(n,C.c_size_t) for n in ('peak','working','peak_paged','paged','peak_nonpaged','nonpaged','pagefile','peak_pagefile')]
def memory():
    p=Memory();p.cb=C.sizeof(p);C.windll.kernel32.GetCurrentProcess.restype=C.c_void_p;C.windll.psapi.GetProcessMemoryInfo.argtypes=[C.c_void_p,C.POINTER(Memory),C.c_ulong];ok=C.windll.psapi.GetProcessMemoryInfo(C.windll.kernel32.GetCurrentProcess(),C.byref(p),C.sizeof(p));assert ok;return dict(working_mib=round(p.working/1048576,3),private_mib=round(p.pagefile/1048576,3))
def timing(values):return dict(mean_ms=round(statistics.mean(values),3),p95_ms=round(float(np.percentile(values,95)),3),max_ms=round(max(values),3))
def main():
    library=json.loads((ROOT/'graphics/portraits/library.json').read_text())['portraits'];assets=[p for p in library if p.get('archive_img')][:40]
    hud=Image.open(ROOT/'test_current/robot/native_65040.png').convert('RGBA').crop((0,136,56,184));natives=[]
    for item in assets:
        a=np.zeros((192,256,3),dtype='uint8');a[136:184,:56]=np.asarray(Image.alpha_composite(hud,Image.open(ROOT/'graphics'/item['portrait_mask']).convert('RGBA')).convert('RGB'));natives.append(a)
    surfaces=[Image.new('RGB',(1440,1080)),Image.new('RGB',(1440,1080))];before=memory();init=[];renderers=[]
    for _ in range(2):
        start=time.perf_counter();renderers.append(PortraitRenderer());init.append((time.perf_counter()-start)*1000)
    after_init=memory();cold=[];opened=[];original_open=Image.open
    main_thread=threading.get_ident()
    def tracked(*a,**kw):opened.append(dict(path=str(a[0]),render_thread=threading.get_ident()==main_thread));return original_open(*a,**kw)
    with patch('PIL.Image.open',tracked):
        for native in natives[:24]:
            start=time.perf_counter()
            for r,s in zip(renderers,surfaces):r.compose(s,native)
            cold.append((time.perf_counter()-start)*1000)
            until=time.perf_counter()+5
            while not all(r.cache.get(r.fastmatch[0]['path']) is not None for r in renderers):
                for r in renderers:r.collect_prepared()
                assert time.perf_counter()<until
                time.sleep(.001)
    cold_reads=len(opened);cold_main_reads=sum(x['render_thread'] for x in opened);cold_main_hd_reads=sum(x['render_thread'] and x['path'].endswith('_hd.png') for x in opened);opened.clear();warm=[];native=natives[23]
    with patch('PIL.Image.open',tracked):
        for _ in range(300):
            start=time.perf_counter()
            for r,s in zip(renderers,surfaces):assert r.compose(s,native)
            warm.append((time.perf_counter()-start)*1000)
    warm_reads=len(opened);opened.clear();miss=[];blank=np.zeros((192,256,3),dtype='uint8')
    with patch('PIL.Image.open',tracked):
        for _ in range(300):
            start=time.perf_counter()
            for r,s in zip(renderers,surfaces):assert not r.compose(s,blank)
            miss.append((time.perf_counter()-start)*1000)
    miss_reads=len(opened);after_warm=memory()
    for native in natives:
        for r,s in zip(renderers,surfaces):r.compose(s,native)
    until=time.perf_counter()+5
    while any(r.pending for r in renderers):
        for r in renderers:r.collect_prepared()
        assert time.perf_counter()<until
        time.sleep(.001)
    after_full=memory();result=dict(renderers=2,registered_each=len(library),constructor_ms=init,memory_before=before,memory_after_init=after_init,memory_after_warm=after_warm,memory_after_40_faces=after_full,cold_pair=timing(cold),cold_file_reads=cold_reads,cold_render_thread_reference_reads=cold_main_reads,cold_render_thread_hd_reads=cold_main_hd_reads,warm_pair=timing(warm),warm_file_reads=warm_reads,miss_pair=timing(miss),miss_file_reads=miss_reads,hd_cache_sizes=[len(r.cache) for r in renderers],reference_cache_sizes=[len(r.references) for r in renderers],note='Cold means empty application asset cache; Windows filesystem cache is not forcibly cleared.')
    assert warm_reads==0 and miss_reads==0 and cold_main_hd_reads==0
    (OUT/'performance_two_screens.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
if __name__=='__main__':main()
