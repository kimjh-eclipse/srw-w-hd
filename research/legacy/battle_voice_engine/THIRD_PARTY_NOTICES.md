# Third-Party Notices

The project source is licensed under the terms in [`LICENSE`](LICENSE). Those
terms do not replace the licenses of external programs or user-provided data.

## External build and runtime tools

The repository does not contain these programs:

- **FFmpeg** is invoked to decode and normalize user-provided audio. The exact
  FFmpeg build may be LGPL-2.1-or-later, GPL-2.0-or-later, or include additional
  codec terms. See <https://ffmpeg.org/legal.html>.
- **devkitPro devkitARM** supplies `arm-none-eabi-gcc`, `objcopy`, and `nm` for
  the freestanding ARM9 payload. This repository contains no devkitARM, GCC,
  binutils, libnds, or Nintendo SDK file. See <https://devkitpro.org/>.
- **CPython** runs the application. See <https://docs.python.org/3/license.html>.
- **Tcl/Tk** is used through Python's `tkinter` module for the GUI. See
  <https://www.tcl-lang.org/software/tcltk/license.html>.
- **PyInstaller** is used to produce the optional Windows single-file release
  executables. Its GPL-2.0-or-later license includes a bootloader exception that
  permits generated applications to retain their own license. See
  <https://pyinstaller.org/en/stable/license.html>.
- **OpenSSL libcrypto** can be included by the Python runtime for hashing
  support. OpenSSL 3.x is licensed under Apache-2.0. See
  <https://www.openssl.org/source/license.html>.
- **Microsoft Visual C++ Runtime** files required by CPython can be included in
  Windows executables under Microsoft's redistributable terms. See
  <https://learn.microsoft.com/cpp/windows/redistributing-visual-cpp-files>.

The 3.0.0 Windows build was produced with CPython 3.12.14, Tcl/Tk 8.6.12,
PyInstaller 6.21.0, and OpenSSL 3.5.8. Rebuilders must inspect their generated
executables and update this notice if dependency versions change.

## Game and user-provided content

Nintendo DS, Super Robot Wars W, and related names, trademarks, game data,
artwork, and music belong to their respective owners. They are mentioned only
to identify compatibility.

This distribution contains no ROM, extracted game data, copyrighted music,
official Nintendo SDK component, FFmpeg binary, or devkitARM package. Users
must provide their own lawfully obtained ROM and authorized audio. Generated
ROMs, BPS files, and BGM packages can contain or encode user-provided
copyrighted material; users are responsible for whether those outputs may be
distributed.

This notice is informational and is not legal advice.
