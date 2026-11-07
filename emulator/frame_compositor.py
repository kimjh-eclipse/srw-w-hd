"""Immutable snapshots cross a process boundary, keeping emulation responsive."""
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp,os,queue
from collections import deque
from frame_process import start_frame_worker,render_snapshot,close_frame_worker
from render_resolution import DEFAULT_WIDTH

class ReadyParts:
    def __init__(self):self.ready_generation=-1;self.values=[];self.dynamic_bindings=queue.SimpleQueue()
    def ready_bindings(self):return self.values

class FrameCompositor:
    def __init__(self,async_parts=True,dynamic_parts=True,memory_name=None,lock=None):
        self.bottom_revision=0;self.render_width=DEFAULT_WIDTH;self.render_size=(DEFAULT_WIDTH,DEFAULT_WIDTH*3//4);self.dynamic_parts=dynamic_parts;self.ready=ReadyParts();self.future=None;self.needs_refresh=False
        self.render_times=deque(maxlen=120)
        self.executor=ProcessPoolExecutor(max_workers=1,mp_context=mp.get_context('spawn'),initializer=start_frame_worker,initargs=(os.getpid(),async_parts,dynamic_parts,memory_name,lock))
    def snapshot(self,core,paused,frame):
        kwargs=dict(robot=tuple(core.robot),obj=bytes(core.obj.raw),parts=core.parts.copy(),owners=core.owners.copy(),bgpriors=core.bgpriors.copy(),bgparts=core.bgparts.copy(),part_palettes=core.part_palettes.copy(),backgrounds=list(core.backgrounds))
        kwargs['render_width']=self.render_width
        kwargs['bg_layout']=list(core.bg_layout)
        if self.dynamic_parts:kwargs['unknown']=core.unknown_snapshot()
        return core.native.copy(),core.ids.copy(),tuple(core.hd),paused,frame,kwargs
    def submit(self,core,paused,frame):self.future=self.executor.submit(render_snapshot,self.snapshot(core,paused,frame))
    def update(self,ready):
        generation,values,dynamic,pending,*extra=ready
        if extra:self.bottom_revision=extra[0]
        if len(extra)>1:self.render_size=tuple(extra[1])
        if len(extra)>2:self.render_times.append(float(extra[2]))
        if generation>=self.ready.ready_generation:
            self.ready.ready_generation=generation;self.needs_refresh=pending
            if values is not None:self.ready.values=values
        for binding in dynamic:self.ready.dynamic_bindings.put(binding)
    def take(self):
        if self.future is None or not self.future.done():return None
        result,ready=self.future.result();self.future=None;self.update(ready);return result
    def capture(self,core,paused):
        image,ready=self.executor.submit(render_snapshot,self.snapshot(core,paused,0),True).result();self.update(ready);return image
    def close(self):
        try:self.executor.submit(close_frame_worker).result(timeout=1)
        except Exception:pass
        for process in list((self.executor._processes or {}).values()):
            if process.is_alive():process.terminate()
        self.executor.shutdown(wait=True,cancel_futures=False)
