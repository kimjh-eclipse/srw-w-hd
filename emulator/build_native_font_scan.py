"""Build the standalone exact glyph scanner; does not rebuild the HD core."""
from pathlib import Path
import subprocess
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    compiler=HERE.parent/'tools/w64devkit/bin/gcc.exe'
    command=[str(compiler),'-O3','-DNDEBUG','-std=c11','-shared','-s','-o',str(HERE/'native_font_scan.dll'),str(HERE/'native_font_scan.c')]
    subprocess.run(command,check=True);print(HERE/'native_font_scan.dll')
