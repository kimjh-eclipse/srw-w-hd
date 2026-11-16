#!/bin/sh
# Wait until no other library writer runs, then apply eye reviews for the given units.
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'apply_eye_review|install_unit_sets|install_pending_art' }) { exit 0 } else { exit 1 }"; do sleep 30; done
py -3.11 -X utf8 scripts/assets/apply_eye_review.py "$@"
