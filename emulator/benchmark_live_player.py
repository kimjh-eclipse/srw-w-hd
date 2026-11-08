"""Measure the actual desktop player with isolated settings and a fixed replay."""
import argparse,json,time,multiprocessing as mp
import tkinter as tk
from types import SimpleNamespace
from hd_emulator import EmulatorWindow,ROOT,CANONICAL
from player_controls import DEFAULTS
import copy

def main():
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    parser=argparse.ArgumentParser();parser.add_argument('--fixed',action='store_true');parser.add_argument('--seconds',type=int,default=40);parser.add_argument('--profile',action='store_true');parser.add_argument('--geometry',default='1280x874');parser.add_argument('--width',type=int,default=768);parser.add_argument('--state',type=__import__('pathlib').Path,default=ROOT/'test_current/font/cutin_dialogue.state');parser.add_argument('--state-frame',type=int,default=65272);parser.add_argument('--label');args=parser.parse_args()
    out=ROOT/'test_current/performance';mode=args.label or ('full' if args.fixed else 'adaptive');config=out/f'live_{mode}_settings.json'
    settings=copy.deepcopy(DEFAULTS);settings.update(geometry=args.geometry,layout='large_horizontal',swap=False,volume=0,hd_auto_quality=not args.fixed)
    config.write_text(json.dumps(settings));metrics=out/f'live_{mode}_metrics.json'
    options=SimpleNamespace(config=config,save_root=out/'live_saves',metrics=metrics,profile_render=out/f'live_{mode}_profile.txt' if args.profile else None,software_display=False,legacy_timing=False,no_start=True,demo=False,rom=None,state=None,state_frame=args.state_frame,paused=False)
    root=tk.Tk();app=EmulatorWindow(root,options)
    if args.fixed:app.desired_render_width=lambda:args.width
    state=dict(start=None)
    def check():
        check_start=time.perf_counter()
        root.title('HD 속도 측정 · '+mode)
        if app.metrics.detail_path:app.metrics.checks.append(dict(start=check_start,title_ms=(time.perf_counter()-check_start)*1000))
        if app.loaded and app.latest and state['start'] is None:state['start']=time.perf_counter();app.canvas.focus_force()
        if state['start'] is not None and time.perf_counter()-state['start']>=args.seconds:
            rows=[r for r in app.metrics.history if r.get('emulation_fps',0)>40 and r['display_fps']>1]
            foreground=[r for r in rows if r.get('foreground')]
            def average(key,items):return round(sum(r[key] for r in items if r.get(key) is not None)/max(1,sum(r.get(key) is not None for r in items)),3)
            report=dict(mode=mode,samples=len(rows),foreground_samples=len(foreground),display_fps=average('display_fps',rows),foreground_fps=average('display_fps',foreground) if foreground else None,composition_fps=average('composition_fps',rows),emulation_fps=average('emulation_fps',rows),display_ms=average('display_ms',rows),render_width=app.latest[0].width)
            (out/f'live_{mode}_result.json').write_text(json.dumps(report,indent=2));app.metrics.save_detail();print(json.dumps(report),flush=True);app.close();return
        root.after(500,check)
    def start():app.start_session(CANONICAL,True,args.state,args.state_frame,False)
    root.after(100,start);root.after(200,check);root.mainloop()

if __name__=='__main__':mp.freeze_support();main()
