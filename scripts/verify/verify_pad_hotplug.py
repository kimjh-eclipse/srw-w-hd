"""Compatibility entry point for isolated controller hotplug regression checks."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from scripts.verify.verify_pad_process import main

if __name__=='__main__':main()
