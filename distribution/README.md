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

`prepare_images.py` keeps native recognition/approved seed PNGs unchanged. Other
art is packaged as WebP, at most 960 pixels on its longest side, with RGB
precision bounded to 2/255 and alpha preserved exactly after sizing. Every
encoded file is decoded again and checked. Original editing PNGs stay in the
source workspace. `AssetPath` resolves catalog PNG names to packaged WebP files.

Decoded assets share a 1 GiB stage cache. Normal small working-set eviction
retains the object until the next exactly recognized chapter title, unless the
global cap is exceeded: then the least recently used asset is removed. A small
batch of related unit parts is prefetched after current visible requests finish.
Resolution changes retain decoded assets; resolution-dependent textures use
separate keys. `SRWW_STAGE_CACHE_MB` can override the cap for testing.

`archive_portable.py` produces a complete ZIP plus separate Program/Assets ZIPs
for GitHub Releases. Extract both separate ZIPs into the same directory. Keep
the user's `data` directory when updating. These archives follow the release
manifest and cannot contain ROMs, states, battery saves, settings or logs.
