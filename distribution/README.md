# Windows portable distribution

Run `python distribution/build_portable.py` on Windows after installing
`distribution/requirements-build.txt`. The local GPU dependencies must also be
available under `tools/gpu_py` (`moderngl==5.12.0`, `glcontext==3.0.0`).

Output: `dist/SRW_W_HD/SRW_W_HD.exe`, its `_internal` dependencies and external
`graphics` directory. Keep these together. No separate Python installation is
needed by the player. Windows Korean font support (Malgun Gothic) is required.
The supplied DeSmuME DLL must be built from the included project sources before
packaging; see the emulator build instructions. No debug interpreter is shipped.

ROMs, save states, generated texture cache and personal settings are excluded
from the distribution manifest. Users select their own supported Korean 1.0.8
ROM. A `portable.txt` marker places new settings, saves, cache and logs in `data`;
without it the application uses `%LOCALAPPDATA%/SRW_W_HD`. Preserve user data
when updating. The development battle preview requires a private state and is
disabled in the frozen application.

`--self-test REPORT.json --rom PATH --state PATH` tests the frozen process tree,
including controller and texture workers, with external private fixtures. Do not
include those private fixtures or the resulting `data` directory in an archive.
The matching frontend/core source and license notices are included in the output.

Menu regression checks: `emulator/verify_selected_text_beds.py` tests opaque glyph
beds and changing selections. `emulator/verify_menu_runtime.py` also warms real
asynchronous dynamic textures and sends their ready bindings back to the native
core: the menu must remain correct after the first frame, not merely when paused.
Horizontal 16-pixel button ramps are kept out of robot texture matching so the
font renderer retains the actual selection backdrop on both displays.
