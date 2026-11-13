"""Immutable snapshots cross a process boundary, keeping emulation responsive."""
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp,os,queue,time
from collections import deque
from frame_process import start_frame_worker,render_snapshot,close_frame_worker,stream_frames
from render_resolution import DEFAULT_WIDTH

class ReadyParts:
    def __init__(self):self.ready_generation=-1;self.values=[];self.dynamic_bindings=queue.SimpleQueue()
    def ready_bindings(self):return self.values

class FrameCompositor:
    def __init__(self,async_parts=True,dynamic_parts=True,memory_name=None,lock=None,present=None):
        self.bottom_revision=0;self.render_width=DEFAULT_WIDTH;self.render_size=(DEFAULT_WIDTH,DEFAULT_WIDTH*3//4);self.dynamic_parts=dynamic_parts;self.ready=ReadyParts();self.future=None;self.needs_refresh=False
        self.render_times=deque(maxlen=120);self.layout=dict(present) if present else None
        self.streaming=bool(memory_name) and os.environ.get('SRWW_STREAMING_FRAMES','1')!='0'
        ctx=mp.get_context('spawn')
        if self.streaming:
            # Only one waiting snapshot: slow rendering cannot accumulate an
            # ever older input/video backlog. The running frame is independent.
            self.requests=ctx.Queue(maxsize=1);self.replies,child=ctx.Pipe(duplex=False)
            self.process=ctx.Process(target=stream_frames,args=(os.getpid(),async_parts,dynamic_parts,memory_name,lock,self.requests,child,present.get('hwnd') if present else None))
            self.process.start();child.close();self.executor=None
        else:
            self.executor=ProcessPoolExecutor(max_workers=1,mp_context=ctx,initializer=start_frame_worker,initargs=(os.getpid(),async_parts,dynamic_parts,memory_name,lock))
    def snapshot(self,core,paused,frame):
        kwargs=dict(robot=tuple(core.robot),obj=bytes(core.obj.raw),parts=core.parts.copy(),owners=core.owners.copy(),bgpriors=core.bgpriors.copy(),bgparts=core.bgparts.copy(),part_palettes=core.part_palettes.copy(),backgrounds=list(core.backgrounds))
        kwargs['render_width']=self.render_width
        if self.layout is not None and self.streaming:kwargs['present_layout']=self.layout
        kwargs['bg_layout']=list(core.bg_layout)
        kwargs['cutin_layers']=core.cutin_layers.copy()
        kwargs['effect_foreground']=core.effect_foreground.copy() if core.effect_foreground is not None else None
        window=getattr(core,'window',None);kwargs['window']=window.copy() if window is not None else None
        kwargs['cutin_palettes']=getattr(core,'cutin_palettes',None)
        kwargs['sub_parts']=(core.sub_parts.copy(),core.sub_owners.copy(),bytes(core.sub_oam.raw),core.sub_palettes.copy(),core.sub_ids.copy(),core.sub_priorities.copy()) if core.sub_bridge else None
        if self.dynamic_parts:kwargs['unknown']=core.unknown_snapshot()
        return core.native.copy(),core.ids.copy(),tuple(core.hd),paused,frame,kwargs
    def submit(self,core,paused,frame):
        if self.streaming:
            if self.requests.full():return False
            snapshot=self.snapshot(core,paused,frame)
            try:self.requests.put_nowait(('render',snapshot))
            except queue.Full:return False
        else:self.future=self.executor.submit(render_snapshot,self.snapshot(core,paused,frame))
        return True
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
        if self.streaming:
            if not self.replies.poll():
                if not self.process.is_alive():raise RuntimeError('HD composition process stopped')
                return None
            kind,result,ready=self.replies.recv()
            if kind=='error':raise RuntimeError(result)
            self.update(ready);return result
        if self.future is None or not self.future.done():return None
        result,ready=self.future.result();self.future=None;self.update(ready);return result
    def capture(self,core,paused):
        if self.streaming:
            request=('capture',self.snapshot(core,paused,0))
            # Drain replies while waiting for a queue slot. A large ready-part
            # update can otherwise block the child's pipe and deadlock capture.
            while True:
                try:self.requests.put_nowait(request);break
                except queue.Full:
                    if self.replies.poll(.01):
                        kind,result,ready=self.replies.recv()
                        if kind=='error':raise RuntimeError(result)
                        self.update(ready)
                    elif not self.process.is_alive():raise RuntimeError('HD composition process stopped')
            while True:
                kind,result,ready=self.replies.recv()
                if kind=='error':raise RuntimeError(result)
                self.update(ready)
                if kind=='capture':return result
        image,ready=self.executor.submit(render_snapshot,self.snapshot(core,paused,0),True).result();self.update(ready);return image
    def close(self):
        if self.streaming:
            # A full waiting-frame slot must not discard the shutdown signal.
            # Keep draining replies so the renderer can finish and save traces.
            deadline=time.monotonic()+1.5;sent=False
            while self.process.is_alive() and time.monotonic()<deadline:
                if not sent:
                    try:self.requests.put_nowait(None);sent=True
                    except queue.Full:pass
                try:
                    if self.replies.poll(.01):self.replies.recv()
                    elif sent:self.process.join(timeout=.01)
                except (EOFError,OSError):break
            self.process.join(timeout=.05)
            if self.process.is_alive():self.process.terminate();self.process.join(timeout=2)
            self.replies.close();self.requests.cancel_join_thread();self.requests.close();return
        try:self.executor.submit(close_frame_worker).result(timeout=1)
        except Exception:pass
        for process in list((self.executor._processes or {}).values()):
            if process.is_alive():process.terminate()
        self.executor.shutdown(wait=True,cancel_futures=False)
