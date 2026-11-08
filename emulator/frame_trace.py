"""Opt-in in-memory stage timings, flushed once outside measured playback."""
import json,os,time,gc
from pathlib import Path

class FrameTrace:
    def __init__(self,path):
        self.path=Path(path);self.rows=[];self.current=None;self.collections=[]
        self.gc_start=None
        def collection(phase,info):
            if phase=='start':self.gc_start=time.perf_counter()
            elif self.gc_start is not None:self.collections.append(dict(time=self.gc_start,ms=(time.perf_counter()-self.gc_start)*1000,generation=info['generation'],collected=info['collected']))
        self.gc_callback=collection;gc.callbacks.append(collection)
    def begin(self,frame):self.current=dict(frame=frame,start=time.perf_counter(),stages={})
    def wrap(self,obj,name,label):
        original=getattr(obj,name)
        def timed(*args,**kwargs):
            start=time.perf_counter()
            try:return original(*args,**kwargs)
            finally:
                if self.current is not None:
                    stages=self.current['stages'];stages[label]=stages.get(label,0)+(time.perf_counter()-start)*1000
        setattr(obj,name,timed)
    def finish(self):
        row=self.current
        if row is not None:
            row['ms']=(time.perf_counter()-row['start'])*1000
            if len(self.rows)<10000:self.rows.append(row)
        self.current=None
    def save(self):
        self.path.parent.mkdir(parents=True,exist_ok=True);self.path.write_text(json.dumps(dict(frames=self.rows,gc=self.collections)),encoding='utf-8')

def install(renderer):
    path=os.environ.get('SRWW_FRAME_TRACE')
    if not path:return None
    trace=FrameTrace(path)
    for obj,name,label in [(renderer,'render_top','top'),(renderer,'render_bottom','bottom'),
        (renderer.text_renderer,'recognize','font_scan'),(renderer.text_renderer,'compose','font_paint'),
        (renderer.text_renderer,'_glyph','glyph'),(renderer.text_renderer,'_heal_plan','heal_plan'),
        (renderer.bottom_text_renderer,'compose','bottom_font'),(renderer.bottom_text_renderer,'recognize','bottom_font_scan'),
        (renderer.parts_renderer,'compose','parts'),(renderer.battle_backgrounds,'compose','battle_bg'),
        (renderer.backgrounds,'compose','legacy_bg'),(renderer.scenario_backgrounds,'compose','scenario'),
        (renderer.map_tiles,'compose','map'),(renderer.map_icons,'compose','icons'),
        (renderer.portraits,'compose','portraits'),(renderer.ui_labels,'compose','labels')]:trace.wrap(obj,name,label)
    if renderer.gpu_composition:
        from gpu_surface import backend
        trace.wrap(backend(),'render','gpu_draw_read')
    return trace
