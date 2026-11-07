@echo off
rem This Source Code Form is subject to the terms of the Mozilla Public
rem License, v. 2.0. If a copy of the MPL was not distributed with this
rem file, You can obtain one at https://mozilla.org/MPL/2.0/.
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"

if not exist ".venv\Scripts\python.exe" (
  echo Creating release build environment...
  python -m venv .venv
  if errorlevel 1 goto :error
)

".venv\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto :error
".venv\Scripts\python.exe" build_release.py
if errorlevel 1 goto :error

echo.
echo Release files are in: %~dp0dist
pause
exit /b 0

:error
echo.
echo Release build failed.
pause
exit /b 1
