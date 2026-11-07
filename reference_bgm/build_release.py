# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tkinter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"
BUILD = ROOT / "release_build"
VERSION = "3.0.0"

APPLICATIONS = (
    ("SRW_W_BGM_Pack_Maker", ROOT / "packaging_entry" / "pack_maker_entry.py"),
    ("SRW_W_BGM_ROM_Patcher", ROOT / "packaging_entry" / "rom_patcher_entry.py"),
)

RUNTIME_DATA = (
    ROOT / "bgm_catalog.json",
    ROOT / "LICENSE",
    ROOT / "THIRD_PARTY_NOTICES.md",
    ROOT / "README.md",
    ROOT / "README.en.md",
    ROOT / "AUTHORS.md",
)


def run(command: list[str]) -> None:
    print(" ".join(command), flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def add_data_argument(source: Path, destination: str) -> str:
    return f"{source}{';' if sys.platform == 'win32' else ':'}{destination}"


def verify_tkinter() -> None:
    try:
        interpreter = tkinter.Tcl()
        interpreter.eval("info library")
    except tkinter.TclError as exc:
        raise RuntimeError(
            "Tcl/Tk runtime is incomplete. Build with a standard Python.org "
            "Windows installation; refusing to create an EXE without tkinter."
        ) from exc


def build_application(name: str, entry: Path) -> Path:
    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--windowed",
        "--noupx",
        "--name",
        name,
        "--distpath",
        str(DIST),
        "--workpath",
        str(BUILD / "work" / name),
        "--specpath",
        str(BUILD / "spec"),
        "--paths",
        str(ROOT),
        "--add-data",
        add_data_argument(ROOT / "src", "src"),
    ]
    for path in RUNTIME_DATA:
        command.extend(["--add-data", add_data_argument(path, ".")])
    command.append(str(entry))
    run(command)
    output = DIST / f"{name}.exe"
    if not output.is_file():
        raise RuntimeError(f"PyInstaller output is missing: {output}")
    return output


def write_checksums(outputs: list[Path]) -> None:
    lines = []
    for output in outputs:
        digest = hashlib.sha256(output.read_bytes()).hexdigest()
        lines.append(f"{digest}  {output.name}")
    lines.append("")
    (DIST / "SHA256SUMS.txt").write_text("\n".join(lines), encoding="ascii")


def main() -> int:
    verify_tkinter()
    if BUILD.exists():
        shutil.rmtree(BUILD)
    DIST.mkdir(parents=True, exist_ok=True)
    for stale in DIST.glob("SRW_W_BGM_*.exe"):
        stale.unlink()
    outputs = [build_application(name, entry) for name, entry in APPLICATIONS]
    write_checksums(outputs)
    print(f"Release {VERSION}")
    for output in outputs:
        print(f"{output.name}: {output.stat().st_size:,} bytes")
    print(f"Checksums: {DIST / 'SHA256SUMS.txt'}")
    print("Bundled ROM/audio/FFmpeg/devkitARM/Nintendo SDK: NO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
