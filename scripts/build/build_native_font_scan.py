"""Build the standalone exact glyph scanner; does not rebuild the HD core."""

import sys as _sys
from pathlib import Path as _Path
_sys.path.insert(0, str(_Path(__file__).resolve().parents[2]))
from scripts._bootstrap import ROOT as PROJECT_ROOT

from pathlib import Path
import subprocess
HERE=(PROJECT_ROOT/'emulator')
if __name__=='__main__':
    compiler=HERE.parent/'tools/w64devkit/bin/gcc.exe'
    command=[str(compiler),'-O3','-DNDEBUG','-std=c11','-shared','-s','-o',str(HERE/'native_font_scan.dll'),str(HERE/'native_font_scan.c')]
    subprocess.run(command,check=True);print(HERE/'native_font_scan.dll')
