"""Bounded HD resolution adjustment for the native 59.8261 Hz frame budget."""
from collections import deque
import time
from render_resolution import clamp_width

class RenderBudget:
    def __init__(self,width,enabled=True):
        self.maximum=clamp_width(width);self.width=self.maximum;self.enabled=bool(enabled)
        self.samples=deque(maxlen=90);self.changed=time.monotonic()

    def configure(self,width=None,enabled=None):
        if width is not None:self.maximum=clamp_width(width)
        if enabled is not None:self.enabled=bool(enabled)
        self.width=min(self.width,self.maximum) if self.enabled else self.maximum
        self.samples.clear();self.changed=time.monotonic()
        return self.width

    def observe(self,milliseconds,now=None):
        if not self.enabled:return self.maximum
        now=time.monotonic() if now is None else now
        self.samples.append(float(milliseconds))
        if len(self.samples)<60 or now-self.changed<4:return self.width
        values=sorted(self.samples);mean=sum(values)/len(values);p90=values[int(len(values)*.9)]
        minimum=min(768,self.maximum);width=self.width
        if mean>11 or (mean>9 and p90>16):width=max(minimum,self.width-128)
        elif mean<6 and p90<10 and now-self.changed>=30:width=min(self.maximum,self.width+64)
        if width!=self.width:self.width=width;self.samples.clear();self.changed=now
        return self.width
