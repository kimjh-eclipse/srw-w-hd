# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from __future__ import annotations

import ctypes
import os
import sys
import tempfile
import traceback
from pathlib import Path


DEFAULT_ROM_NAMES = (
    "0870 - Super Robot Taisen W (kor)_2.0.3.nds",
    "0870 - Super Robot Taisen W (k).nds",
)


def executable_directory() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def configure_defaults() -> None:
    base = executable_directory()
    os.environ.setdefault("SRWW_DEFAULT_OUTPUT", str(base / "out"))
    for name in DEFAULT_ROM_NAMES:
        candidate = base / name
        if candidate.is_file():
            os.environ.setdefault("SRWW_DEFAULT_ROM", str(candidate))
            break


def report_startup_error(mode: str) -> None:
    detail = traceback.format_exc()
    log_path = Path(tempfile.gettempdir()) / f"SRW_W_BGM_{mode}_error.log"
    log_path.write_text(detail, encoding="utf-8")
    message = f"프로그램을 시작하지 못했습니다.\n\n{detail}\n로그: {log_path}"
    try:
        ctypes.windll.user32.MessageBoxW(None, message, "SRW W BGM 도구 오류", 0x10)
    except Exception:
        sys.stderr.write(message + "\n")


def run(mode: str) -> int:
    configure_defaults()
    try:
        from app_gui import main

        return main(mode=mode, self_test="--self-test" in sys.argv)
    except Exception:
        report_startup_error(mode)
        return 1
