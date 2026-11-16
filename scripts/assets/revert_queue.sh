#!/bin/sh
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
LOCK=test_current/parts/pose_packets/.install_lock
until mkdir "$LOCK" 2>/dev/null; do sleep 20; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT INT TERM
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'apply_eye_review|install_unit_sets|install_pending_art' }) { exit 0 } else { exit 1 }"; do sleep 20; done
cp graphics/kazuma_parts_library.json test_current/parts/pending_install/kazuma_parts_library.before_revert_14_15_27_28_29.json
cp docs/ART_INSTALL_DONE.json test_current/parts/pending_install/ART_INSTALL_DONE.before_revert.json
py -3.11 -X utf8 scripts/assets/revert_unit_installs.py --unit 14 --before 7611aa73 --unit 15 --before 7611aa73 --unit 27 --before a7333661 --unit 28 --before a7333661 --unit 29 --before a7333661
