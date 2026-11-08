"""Review current installed assets in the real player, with isolated QA saves."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

import argparse,multiprocessing as mp
from pathlib import Path
import tkinter as tk
from types import SimpleNamespace
from hd_emulator import EmulatorWindow,ROOT

def main():
    parser=argparse.ArgumentParser();parser.add_argument('scene',choices=['favorite','introduction','earth','map','chapter']);parser.add_argument('--state',type=Path);args=parser.parse_args()
    states=dict(favorite='formation/formation.state',introduction='formation/favorite_base.state',earth='scenario/final.state',map='map_icons/all_enemies_visible.state',chapter='localized_screens/chapter.state')
    out=ROOT/'test_current/menu_card'
    options=SimpleNamespace(config=out/'review_settings.json',save_root=out/'review_saves',metrics=out/f'review_{args.scene}_metrics.json',profile_render=None,software_display=False,legacy_timing=False,no_start=False,demo=False,rom=None,state=args.state or ROOT/'test_current'/states[args.scene],state_frame=0,paused=True)
    root=tk.Tk();app=EmulatorWindow(root,options)
    def label():
        if app.closed:return
        root.title('HD 적용 확인 · '+args.scene)
        root.after(500,label)
    root.after(250,label);root.mainloop()

if __name__=='__main__':mp.freeze_support();main()
