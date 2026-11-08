"""Launch the desktop player from the repository root."""
from pathlib import Path
import multiprocessing
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent/'emulator'))

if __name__ == '__main__':
    multiprocessing.freeze_support()
    from hd_emulator import main
    main()
