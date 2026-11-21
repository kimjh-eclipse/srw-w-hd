#!/bin/sh
# Soft-edge rollout (11/20): re-split/package/install every installed unit with the outline ring
# (split_object_drawings EDGE_RING), then redo the one-owner family installs on top.
# Resumable: units already redone are listed in _smooth_done.txt and skipped. 20 units per
# install_unit_sets call (caches are rebuilt once per call).
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
B=test_current/parts/pose_packets;LOCK=$B/.install_lock;DONE=$B/_smooth_done.txt;touch $DONE
until mkdir "$LOCK" 2>/dev/null; do sleep 20; done
trap 'rmdir "$LOCK" 2>/dev/null' EXIT INT TERM
[ -f graphics/kazuma_parts_library.before_smooth_rollout.json ] || cp graphics/kazuma_parts_library.json graphics/kazuma_parts_library.before_smooth_rollout.json
TODO=""
for d in $B/unit_*/robot_set; do
  [ -f $d/INSTALLED ] || continue
  u=${d#$B/unit_};u=${u%%/*}
  grep -qx "$u" $DONE || TODO="$TODO $u"
done
set -- $TODO;echo "$(date +%H:%M) units to redo: $#"
while [ $# -gt 0 ]; do
  CHUNK="";n=0
  while [ $# -gt 0 ] && [ $n -lt 20 ]; do CHUNK="$CHUNK $1";shift;n=$((n+1));done
  echo "$(date +%H:%M) chunk$CHUNK"
  py -3.11 -X utf8 scripts/assets/install_unit_sets.py $CHUNK 2>&1 | grep -E "^[0-9]+ .*(ERROR|NOT INSTALLED|FAILED)" | cut -c1-160
  for u in $CHUNK;do echo $u >> $DONE;done
done
echo "$(date +%H:%M) families"
py -3.11 -X utf8 scripts/assets/strike_owner_install.py 2>&1 | tail -n 2 | cut -c1-160
for f in "54,55,56,57 duel" "323,324,361,367,368,386,392,403 gaogaigar" "53,449 blitz" "70,72,92 din"; do
  set -- $f; py -3.11 -X utf8 scripts/assets/family_owner_install.py --family $1 --tag $2 2>&1 | tail -n 2 | cut -c1-160
done
for s in scripts/build/build_native_material_cache.py scripts/assets/build_material_slot_cache.py scripts/assets/build_tile_library.py; do py -3.11 -X utf8 $s >/dev/null 2>&1 && echo "$s ok" || echo "$s FAILED"; done
echo "$(date +%H:%M) SMOOTH ROLLOUT DONE"
