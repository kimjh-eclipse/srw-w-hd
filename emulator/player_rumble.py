"""Bounded gamepad effects, independent of the game's audio and HD toggle."""
class PadRumble:
    def __init__(self):self.device=None
    def stop(self):
        if self.device:
            try:self.device.stop_rumble()
            except Exception:pass
        self.device=None
    def play(self,device,enabled,strength,low=.65,high=.85,duration=100):
        if not enabled or device is None or strength<=0:self.stop();return False
        if self.device is not device:self.stop()
        try:
            gain=max(0,min(100,float(strength)))/100
            ok=bool(device.rumble(max(0,min(1,low*gain)),max(0,min(1,high*gain)),max(20,min(600,int(duration)))))
            self.device=device if ok else None
            return ok
        except Exception:self.stop();return False
