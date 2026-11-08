
import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import subprocess
HERE=(PROJECT_ROOT/'emulator')
if __name__=='__main__':
    subprocess.run([str(HERE.parent/'tools/w64devkit/bin/gcc.exe'),'-O3','-DNDEBUG','-std=c11','-shared','-s','-o',str(HERE/'native_font_pixels.dll'),str(HERE/'native_font_pixels.c')],check=True)
