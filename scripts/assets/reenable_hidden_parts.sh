#!/bin/sh
# Re-enable reviewed hidden parts under the install lock (same pattern as hidden_parts_queue.sh).
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
LOCK=test_current/parts/pose_packets/.install_lock
until mkdir "$LOCK" 2>/dev/null; do sleep 20; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT INT TERM
while powershell -NoProfile -Command "if (Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -match 'apply_eye_review|install_unit_sets|install_pending_art' }) { exit 0 } else { exit 1 }"; do sleep 20; done
py -3.11 -X utf8 scripts/assets/reenable_hidden_parts.py "$@"
for s in scripts/build/build_native_material_cache.py scripts/assets/build_material_slot_cache.py scripts/assets/build_tile_library.py; do py -3.11 -X utf8 $s >/dev/null 2>&1 && echo "$s ok" || echo "$s FAILED"; done
