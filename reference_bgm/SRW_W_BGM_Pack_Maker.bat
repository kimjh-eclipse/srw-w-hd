@echo off
rem This Source Code Form is subject to the terms of the Mozilla Public
rem License, v. 2.0. If a copy of the MPL was not distributed with this
rem file, You can obtain one at https://mozilla.org/MPL/2.0/.
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
title SRW W BGM Pack Maker - Final ADPCM STRM

if not exist "%~dp0app_gui.py" (
  echo Required file not found: app_gui.py
  pause
  exit /b 1
)

if exist ".venv\Scripts\pythonw.exe" (
  start "SRW W BGM Pack Maker" ".venv\Scripts\pythonw.exe" "%~dp0app_gui.py" --pack
  exit /b 0
)

where pythonw.exe >nul 2>nul
if not errorlevel 1 (
  start "SRW W BGM Pack Maker" pythonw.exe "%~dp0app_gui.py" --pack
  exit /b 0
)

echo Python 3 was not found. Install Python or create .venv first.
pause
exit /b 1
