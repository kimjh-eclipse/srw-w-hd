# SRW W ADPCM STRM Custom BGM Patcher

[한국어](README.md) | [English](README.en.md)

An unofficial open-source toolset that inserts user-supplied audio as ADPCM
STRM custom BGM into the supported Korean 2.0.3 release of **Super Robot Wars W**
for Nintendo DS.

This repository does not contain a ROM, extracted game data, music, FFmpeg,
devkitARM, or any Nintendo SDK component. Users must supply a lawfully obtained
compatible ROM and audio they are authorized to use.

## Features

- Converts FFmpeg-supported audio to 22,050 Hz Nintendo DS IMA-ADPCM STRM
- Supports per-track mono/stereo selection and ROM capacity validation
- Packages up to 70 BGM IDs in an integrity-checked `.bgm.pak` v3 file
- Builds and inserts an ARM9 streaming engine at verified hook/cave locations
- Produces a patched ROM, a distributable BPS file, and a build manifest
- Silences underrun pages during BGM stop and transition handling

## GitHub Release

Download these three files from the [latest Release](../../releases/latest) into
the same directory:

```text
SRW_W_BGM_Pack_Maker.exe
SRW_W_BGM_ROM_Patcher.exe
SHA256SUMS.txt
```

The Windows x64 executables bundle the required Python and Tcl/Tk runtimes, so
end users do not need to install Python. They are unobfuscated single-file
PyInstaller builds produced from this repository's public source.

The executables are not code-signed and may trigger Windows SmartScreen. Check
their SHA-256 hashes against `SHA256SUMS.txt` before running them.

## User requirements

- Windows 10/11
- [FFmpeg](https://ffmpeg.org/download.html) for audio conversion
- [devkitARM](https://devkitpro.org/wiki/Getting_Started) for the ARM9 build
- Supported ROM SHA-256:
  `9cbeacfe4fdbeacd6b0ea070b2f2a583c04018f49a47f1e636d02614988c1287`

FFmpeg and devkitARM are not bundled. libnds and Nintendo SDK files are not
required.

## Quick start

1. Verify the downloaded executable hashes against `SHA256SUMS.txt`.
2. Run `SRW_W_BGM_Pack_Maker.exe`, select FFmpeg and your audio, then create a
   `.bgm.pak`.
3. Run `SRW_W_BGM_ROM_Patcher.exe`, select the compatible ROM, package,
   devkitARM directory, and output directory.
4. Verify the generated ROM and `build_manifest.json` in an emulator.

The two applications are independent. A pack author can distribute only a
`.bgm.pak`, while each user applies it to their own source ROM.

## Running from source

Python 3.10 or later is required only for source use and development. The
application itself uses only the Python standard library.

```powershell
SRW_W_BGM_Pack_Maker.bat
SRW_W_BGM_ROM_Patcher.bat
```

Direct launch is also available through `python app_gui.py --pack` and
`python app_gui.py --patch`.

Run tests with:

```powershell
python -m unittest discover -s tests -v
python -m compileall -q .
```

Run `build_release.bat` to create unobfuscated single-file Windows builds in
`dist/`. Upload both executables, `SHA256SUMS.txt`, and the tagged source archive
to the GitHub Release. ROMs, audio, FFmpeg, devkitARM, and Nintendo SDK files are
not bundled.

## License

The Source Code Form is distributed under the
[Mozilla Public License 2.0](LICENSE). MPL-2.0 applies file-level copyleft:
when a modified covered file is distributed in executable form, its source
must also be made available under MPL-2.0. Separate files in a larger work may
use different terms.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for external tools and
third-party rights, and [CONTRIBUTING.md](CONTRIBUTING.md) before contributing.

This project is not affiliated with or endorsed by Nintendo, Bandai Namco
Entertainment, or Banpresto. Product names and trademarks identify
compatibility only.
