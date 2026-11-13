"""Frozen Windows entry point; dispatch spawned workers before importing the UI."""
import multiprocessing as mp

if __name__=='__main__':
    mp.freeze_support()
    import sys,os,traceback,faulthandler
    from pathlib import Path
    from runtime_paths import log_path
    streams=[]
    for name in ('stdout','stderr'):
        if getattr(sys,name) is None:
            stream=open(log_path(f'{name}_{os.getpid()}.log'),'a',encoding='utf-8',buffering=1);setattr(sys,name,stream);streams.append(stream)
    crash=open(log_path('player_native_crash.log'),'a',encoding='utf-8');faulthandler.enable(file=crash,all_threads=True)
    try:
        if '--self-test' in sys.argv:
            from portable_selftest import main
        elif Path(sys.executable).stem.casefold()=='srw_w_test':
            from unit_review import main
        else:
            from hd_emulator import main
        main()
    except Exception:
        details=traceback.format_exc();log_path('player_ui_error.log').write_text(details,encoding='utf-8')
        if '--self-test' not in sys.argv:
            import tkinter.messagebox as box
            box.showerror('실행 오류','게임 실행 중 오류가 발생했습니다.\n오류 기록: '+str(log_path('player_ui_error.log')))
        raise
