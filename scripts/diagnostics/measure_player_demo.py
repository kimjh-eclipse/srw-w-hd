"""Run the real player on its scripted demo and record what the screen showed.

Starts the same program the user starts, lets the built-in demo play for a
fixed time, saves a screen capture of the window, then asks the window to
close the normal way. Used to compare display paths end to end.
"""
import argparse,ctypes as C,json,os,subprocess,sys,time
from ctypes import wintypes as W
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]


def windows_of(pid):
    user=C.windll.user32;found=[]
    @C.WINFUNCTYPE(C.c_bool,W.HWND,W.LPARAM)
    def visit(hwnd,_):
        owner=W.DWORD();user.GetWindowThreadProcessId(hwnd,C.byref(owner))
        if owner.value==pid and user.IsWindowVisible(hwnd):found.append(hwnd)
        return True
    user.EnumWindows(visit,0);return found


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--name',required=True);parser.add_argument('--seconds',type=float,default=40)
    parser.add_argument('--direct',type=int,default=1);args=parser.parse_args()
    out=ROOT/'test_current/performance/direct_present'/args.name;out.mkdir(parents=True,exist_ok=True)
    environment=dict(os.environ,SRWW_DIRECT_PRESENT=str(args.direct),SRWW_FRAME_TRACE=str(out/'frame_trace.json'))
    process=subprocess.Popen([sys.executable,'-X','utf8',str(ROOT/'run.py'),'--demo','--metrics',str(out/'metrics.json')],cwd=ROOT,env=environment,stdout=open(out/'player.log','w'),stderr=subprocess.STDOUT)
    user=C.windll.user32;shots=0;started=time.perf_counter()
    try:
        while time.perf_counter()-started<args.seconds and process.poll() is None:
            time.sleep(1)
            elapsed=time.perf_counter()-started
            if shots<3 and elapsed>args.seconds*(shots+1)/4+6:
                tops=windows_of(process.pid)
                if tops:
                    rect=W.RECT();user.GetWindowRect(tops[0],C.byref(rect))
                    from PIL import ImageGrab
                    ImageGrab.grab((rect.left,rect.top,rect.right,rect.bottom)).save(out/f'window_{shots}.png');shots+=1
    finally:
        for hwnd in windows_of(process.pid):user.PostMessageW(hwnd,0x0010,0,0)   # WM_CLOSE
        try:process.wait(timeout=20)
        except subprocess.TimeoutExpired:print('window did not close in time; leaving it for the user')
    metrics=json.loads((out/'metrics.json').read_text(encoding='utf-8')) if (out/'metrics.json').exists() else {}
    rows=[h for h in metrics.get('history',[]) if h.get('emulation_fps')]
    def column(name):return sorted(h[name] for h in rows if h.get(name) is not None)
    summary=dict(direct=args.direct,seconds=len(rows),exit_code=process.poll(),screens=shots)
    for name in ('emulation_fps','composition_fps','display_fps','render_ms','render_p95_ms','input_to_present_ms'):
        values=column(name)
        if values:summary[name]=dict(median=round(values[len(values)//2],1),worst=round(values[0] if name.endswith('fps') else values[-1],1))
    status=ROOT/'test_current/performance/gpu_compositor_status.json'
    if status.exists():summary['compositor']=json.loads(status.read_text())
    (out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))


if __name__=='__main__':main()
