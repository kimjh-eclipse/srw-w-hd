"""Exercise the real bounded renderer, shared frame sizes and capture under load."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import json,time
from pathlib import Path
from scripts.verify.verify_player import Session, ROOT

def main():
    session=Session(state=ROOT/'test_current/font/combat_hud.state',state_frame=65800)
    out=ROOT/'test_current/performance';checks={}
    def size(width):
        limit=time.perf_counter()+20
        while time.perf_counter()<limit:
            session.until('frame');image=session.image()
            if image.shape[:2]==(width*3//4,width):return image
        raise AssertionError('resolution did not settle')
    try:
        session.until('loaded');session.send('quality',value=False);image=size(960);assert image.max()>0
        session.send('resolution',width=768);size(768)
        session.send('resolution',width=960);size(960);checks['shared_resolution_boundaries']=True
        session.send('pause',value=False);session.until('paused')
        session.send('input',buttons=[8],sent_at=time.perf_counter());ack=session.until('input_ack');assert ack['applied_at']>=ack['sent_at']
        checks['input_to_emulation_ms']=(ack['applied_at']-ack['sent_at'])*1000
        session.send('input',buttons=[])
        session.send('capture',path=str(out/'stream_capture.png'));session.until('captured',timeout=40);checks['capture_without_deadlock']=True
        session.send('pause',value=True);session.until('paused');session.send('save',slot=1);saved=session.until('saved');assert Path(saved['path']).exists()
        session.send('load',slot=1);assert session.until('state_loaded')['paused'];session.until('frame');checks['pause_save_load']=True
        session.send('hd',value=False);session.until('hd');session.until('frame');assert session.image().max()>0
        session.send('hd',value=True);session.until('hd');session.until('frame');checks['hd_toggle']=True
    finally:session.close()
    checks['clean_process_shutdown']=True
    (out/'streaming_verification.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks))

if __name__=='__main__':main()
