@echo off
rem This Source Code Form is subject to the terms of the Mozilla Public
rem License, v. 2.0. If a copy of the MPL was not distributed with this
rem file, You can obtain one at https://mozilla.org/MPL/2.0/.
setlocal
cd /d "%~dp0"
set "PYTHONUTF8=1"
python -m unittest discover -s tests -v
