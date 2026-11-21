#!/bin/sh
# 11/21 chain: wait for the soft-edge rollout and the re-review disable, then redo the units that
# were cut before the interpolated-cut change (list _smooth_redo_list.txt) with smooth_rollout.sh.
cd "C:/Emul/Workshop/SRW_W_HD" || exit 1
B=test_current/parts/pose_packets
until grep -q "ROLLOUT DONE" $B/_softedge_rollout.log; do sleep 60; done
sleep 120; while [ -d $B/.install_lock ]; do sleep 30; done; sleep 60; while [ -d $B/.install_lock ]; do sleep 30; done
grep -vxF -f $B/_smooth_redo_list.txt $B/_softedge_done.txt > $B/_smooth_done.txt
sh scripts/assets/smooth_rollout.sh > $B/_smooth_rollout.log 2>&1
