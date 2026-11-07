"""Build the isolated DS visibility helper, independently of the emulator DLL."""
from pathlib import Path
import subprocess
HERE=Path(__file__).resolve().parent
if __name__=='__main__':
    subprocess.run([str(HERE.parent/'tools/w64devkit/bin/gcc.exe'),'-O3','-DNDEBUG','-std=c11','-shared','-s','-o',str(HERE/'native_composition.dll'),str(HERE/'native_composition.c')],check=True)
    print(HERE/'native_composition.dll')
