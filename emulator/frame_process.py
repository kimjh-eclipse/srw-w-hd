"""HD composition owns its Python interpreter; native audio never waits on its GIL."""
import os,threading,queue,time
import numpy as np
from render_resolution import SCREEN_RGBA_BYTES,DEFAULT_WIDTH
_renderer=None
_memory=None
_lock=None
_profile=None
_profile_frames=0
_profile_count=0
_last_bottom=None
_last_ready=-1
_trace=None

def start_frame_worker(parent_pid,async_parts,dynamic_parts,memory_name=None,lock=None):
    if os.name=='nt':
        import ctypes as C
        api=C.windll.kernel32;api.GetCurrentProcess.restype=C.c_void_p;api.SetPriorityClass.argtypes=[C.c_void_p,C.c_uint]
        api.SetPriorityClass(api.GetCurrentProcess(),0x20)
        def watch():
            api.OpenProcess.restype=C.c_void_p;handle=api.OpenProcess(0x00100000,False,parent_pid)
            if not handle:os._exit(0)
            api.WaitForSingleObject.argtypes=[C.c_void_p,C.c_uint];api.WaitForSingleObject(handle,0xffffffff);os._exit(0)
        threading.Thread(target=watch,name='HD-frame-parent',daemon=True).start()
    global _profile
    if os.environ.get("SRWW_RENDER_PROFILE"):
        import cProfile
        _profile=cProfile.Profile()
    from hd_renderer import HDRenderer
    global _renderer,_memory,_lock
    if memory_name:
        from multiprocessing import shared_memory
        _memory=shared_memory.SharedMemory(name=memory_name);_lock=lock
    _renderer=HDRenderer(async_parts=async_parts,dynamic_parts=dynamic_parts,gpu_composition=os.environ.get('SRWW_GPU_COMPOSITOR','1')!='0')
    _renderer.text_renderer.prewarm_ui()
    _renderer.ui_labels.prewarm()
    _renderer.parts_renderer.prewarm_registered()
    from frame_trace import install
    global _trace
    _trace=install(_renderer)
    import json
    from pathlib import Path
    capability=Path(__file__).resolve().parent.parent/'test_current/performance/gpu_compositor_status.json'
    try:
        capability.parent.mkdir(parents=True,exist_ok=True)
        capability.write_text(json.dumps(dict(enabled=_renderer.gpu_composition,error=_renderer.gpu_error)))
    except OSError:pass

def render_snapshot(snapshot,full=False):
    global _profile_frames,_profile_count
    started=time.perf_counter()
    if _trace is not None:_trace.begin(snapshot[4])
    profiling=_profile is not None and _profile_frames>=120 and snapshot[4]>=int(os.environ.get('SRWW_PROFILE_MIN_FRAME','0')) and _profile_count<180
    if profiling:_profile.enable()
    try:
        result,ready=_render_snapshot(snapshot,full)
        return result,(*ready,(time.perf_counter()-started)*1000)
    finally:
        if _trace is not None:_trace.finish()
        if _profile is not None:
            _profile.disable();_profile_frames+=1
            if profiling:_profile_count+=1
            if profiling and _profile_count==180:
                import pstats
                with open(os.environ['SRWW_RENDER_PROFILE'],'w',encoding='utf8') as stream:
                    pstats.Stats(_profile,stream=stream).sort_stats('cumtime').print_stats(45)


def _render_snapshot(snapshot,full=False):
    global _last_bottom,_last_ready
    native,ids,hd,paused,frame,kwargs=snapshot
    kwargs=dict(kwargs);_renderer.set_resolution(kwargs.pop('render_width',DEFAULT_WIDTH))
    image=(_renderer.render if full else _renderer.render_top)(native,ids,hd,paused,**kwargs)
    parts=_renderer.parts_renderer;dynamic=[]
    while True:
        try:dynamic.append(parts.dynamic_bindings.get_nowait())
        except queue.Empty:break
    bottom_image=None if full else _renderer.render_bottom(native,hd)
    pending=bool(parts.pending or parts.unmapped_pending or _renderer.portraits.pending or _renderer.backgrounds.pending or _renderer.scenario_backgrounds.pending or _renderer.battle_backgrounds.pending or _renderer.map_tiles.pending or
                 (hasattr(_renderer,'bottom_portraits') and _renderer.bottom_portraits.pending))
    values=parts.ready_bindings() if parts.ready_generation!=_last_ready else None
    _last_ready=parts.ready_generation
    ready=(parts.ready_generation,values,dynamic,pending,getattr(_renderer,'bottom_generation',0),_renderer.size)
    if full:return image,ready
    bottom_pixels=None
    if not paused and hasattr(image,'rgba_pipeline'):
        if hasattr(bottom_image,'ops') and os.environ.get('SRWW_JOINT_READBACK','1')!='0' and not getattr(__import__('gpu_surface').backend(),'paired_disabled',False):
            from gpu_surface import backend
            gpu=backend();tag=(frame,bottom_image,getattr(_renderer,'bottom_generation',0))
            try:
                top,bottom_pixels,(frame,bottom_image,bottom_revision)=gpu.render_pair(image,bottom_image,tag)
            except Exception as error:
                gpu.paired_disabled=True;gpu.paired_error=str(error);gpu.reset_pipeline()
                top,(frame,bottom_image,bottom_revision)=image.rgba_pipeline(tag)
        else:top,(frame,bottom_image,bottom_revision)=image.rgba_pipeline((frame,bottom_image,getattr(_renderer,'bottom_generation',0)))
        ready=(*ready[:4],bottom_revision,ready[5])
        top=top.reshape(-1)
    else:
        if hasattr(image,'rgba'):
            from gpu_surface import backend
            backend().reset_pipeline()
        top=(image.rgba() if hasattr(image,'rgba') else np.asarray(image.convert('RGBA'),dtype='uint8')).reshape(-1)
    bottom_changed=bottom_image is not _last_bottom
    bottom=(bottom_pixels if bottom_pixels is not None else bottom_image.rgba() if hasattr(bottom_image,'rgba') else np.asarray(bottom_image.convert('RGBA'),dtype='uint8')).reshape(-1) if bottom_changed or _memory is None else None
    _last_bottom=bottom_image
    if _memory is not None:
        with _lock:
            np.frombuffer(_memory.buf,dtype='uint8',count=top.size)[:]=top
            if bottom is not None:np.frombuffer(_memory.buf,dtype='uint8',count=bottom.size,offset=SCREEN_RGBA_BYTES)[:]=bottom
            header_offset=SCREEN_RGBA_BYTES*2
            if len(_memory.buf)>=header_offset+16:
                np.frombuffer(_memory.buf,dtype='uint32',count=4,offset=header_offset)[:]=[*_renderer.size,frame,ready[4]]
        return (None,None,frame),ready
    return (top,bottom,frame),ready

def close_frame_worker():
    if _trace is not None:_trace.save()
    if _renderer is not None:
        _renderer.parts_renderer.close();_renderer.backgrounds.close();_renderer.scenario_backgrounds.close();_renderer.map_icons.close();_renderer.map_tiles.close();_renderer.battle_backgrounds.close()
    if _memory is not None:_memory.close()

def stream_frames(parent_pid,async_parts,dynamic_parts,memory_name,lock,requests,replies):
    """Keep the renderer fed without waiting for a future round trip per frame."""
    try:
        start_frame_worker(parent_pid,async_parts,dynamic_parts,memory_name,lock)
        while True:
            request=requests.get()
            if request is None:break
            kind,snapshot=request
            result,ready=render_snapshot(snapshot,full=kind=='capture')
            replies.send((kind,result,ready))
    except (EOFError,BrokenPipeError):pass
    except BaseException:
        import traceback
        try:replies.send(('error',traceback.format_exc(),None))
        except (EOFError,BrokenPipeError,OSError):pass
    finally:
        close_frame_worker();replies.close()
