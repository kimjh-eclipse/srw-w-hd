from pathlib import Path
import subprocess
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    subprocess.run([str(HERE.parent/'tools/w64devkit/bin/gcc.exe'),'-O3','-DNDEBUG','-std=c11','-shared','-s','-o',str(HERE/'native_font_pixels.dll'),str(HERE/'native_font_pixels.c')],check=True)
