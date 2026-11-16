#!/bin/sh
# Apply eye reviews for the given units, one library writer at a time.
# mkdir is atomic: the lock directory is the queue token.
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
LOCK=test_current/parts/pose_packets/.install_lock
until mkdir "$LOCK" 2>/dev/null; do sleep 20; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT INT TERM
# An installer started outside this queue must finish first.
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'apply_eye_review|install_unit_sets|install_pending_art' }) { exit 0 } else { exit 1 }"; do sleep 20; done
py -3.11 -X utf8 scripts/assets/apply_eye_review.py "$@"
