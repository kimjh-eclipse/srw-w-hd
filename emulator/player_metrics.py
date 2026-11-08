"""Optional live GUI/worker measurements; never enabled in normal play."""
import json,time,os,gc
from pathlib import Path


class PlayerMetrics:
    def __init__(self,path):
        self.path=Path(path) if path else None
        self.start=time.perf_counter();self.last=self.start;self.presented=0;self.previous=0
        self.draw_ms=[];self.input_ms=[];self.visible_ms=[];self.pending=[];self.worker={};self.history=[]
        self.last_presented_frame=None
        self.detail_path=os.environ.get('SRWW_UI_TRACE');self.presentations=[];self.polls=[];self.previous_present=None;self.collections=[];self.checks=[]
        if self.detail_path:
            self.gc_start=None
            def collection(phase,info):
                if phase=='start':self.gc_start=time.perf_counter()
                elif self.gc_start is not None:self.collections.append(dict(time=self.gc_start,ms=(time.perf_counter()-self.gc_start)*1000,generation=info['generation'],collected=info['collected']))
            self.gc_callback=collection;gc.callbacks.append(collection)

    def acknowledge(self,message):
        self.input_ms.append((message['applied_at']-message['sent_at'])*1000)
        self.pending.append(message)

    def present(self,frame,milliseconds):
        if self.detail_path and frame!=self.last_presented_frame:
            now=time.perf_counter();self.presentations.append(dict(time=now,frame=frame,interval_ms=(now-self.previous_present)*1000 if self.previous_present else 0,draw_ms=milliseconds));self.previous_present=now
        if frame!=self.last_presented_frame:self.presented+=1;self.last_presented_frame=frame
        self.draw_ms.append(milliseconds)
        now=time.perf_counter()
        for item in self.pending[:]:
            if frame>=item['frame']:
                self.visible_ms.append((now-item['sent_at'])*1000);self.pending.remove(item)

    def update(self,backend):
        if self.path is None:return
        now=time.perf_counter()
        if now-self.last<1:return
        def mean(values):return round(sum(values)/len(values),3) if values else None
        row=dict(elapsed=round(now-self.start,2),display_fps=round((self.presented-self.previous)/(now-self.last),2),
                 display_ms=mean(self.draw_ms),input_to_emulation_ms=mean(self.input_ms),
                 input_to_present_ms=mean(self.visible_ms),backend=backend,**self.worker)
        self.history.append(row);self.path.parent.mkdir(parents=True,exist_ok=True)
        self.path.write_text(json.dumps(dict(latest=row,history=self.history[-1200:]),indent=2),encoding='utf8')
        self.last=now;self.previous=self.presented;self.draw_ms.clear();self.input_ms.clear();self.visible_ms.clear()

    def save_detail(self):
        if self.detail_path:Path(self.detail_path).write_text(json.dumps(dict(presents=self.presentations,polls=self.polls,gc=self.collections,checks=self.checks)),encoding='utf-8')
