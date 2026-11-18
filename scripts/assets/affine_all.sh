#!/bin/sh
# Build affine (scaled/rotated) pose packets and their drawing sheets for every unit whose capture skipped affine sprites.
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
LOG=test_current/parts/pose_packets/AFFINE_BUILD.log
for u in "$@"; do
  rs=test_current/parts/pose_packets/unit_$u/robot_set
  [ -d $rs ] || { echo "$u no robot_set" >> $LOG; continue; }
  [ -d $rs/pose_a00 ] && { echo "$u already" >> $LOG; continue; }
  py -3.11 -X utf8 scripts/assets/build_affine_packets.py $u 2>&1 | grep -E "^(unit|written|no start|Trace|.*Error)" >> $LOG
  ls -d $rs/pose_a* >/dev/null 2>&1 && py -3.11 -X utf8 scripts/assets/pose_sheets.py build $rs --affine >> $LOG 2>&1
done
echo "AFFINE DONE" >> $LOG
