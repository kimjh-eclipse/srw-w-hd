"""Development launcher for the same unit-review UI bundled in SRW_W_Test.exe."""
import multiprocessing as mp
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/"emulator"))
from unit_review import main

if __name__ == "__main__":
    mp.freeze_support()
    main()
