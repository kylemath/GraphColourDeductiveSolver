#!/bin/bash
# s86 (10 Nov 16:40Z): the U86 check of sol_k86GS22_in02 (t 0.0138291824, K3gB5r + 365 + HATBB) cannot get its 2.5 GB memcg slot while
# GS22 (7.7 GB) and GL23 (4.7 GB) both run, and U86 would force-start after 7200 s (OOM risk).  The point is above the sound upper
# 0.013805127581 [E2] (K3l5t), and k's seed-first decision keeps both lanes running to their end, so GL23 is not paused for it:
# this script waits until either lane ends, then runs the same U86 check (same env as watch86e).
N=$(cd $(dirname $0) && pwd)
while pgrep -f 'pcheck.py solveR2.*tag=k86GS2[2] ' > /dev/null && pgrep -f 'pcheck.py solveR2.*tag=k86GL2[3] ' > /dev/null; do sleep 60; done
echo "$(date -u +%H:%M:%SZ) [s86D-k86GS22] a lane ended; running the deferred U86 check of sol_k86GS22_in02" >> $N/run.log
E86OVR=$N/eng_p8h STACK=s77 ARGS=$N/args_A97_F_W13K3gB5r.txt KEYS=$N/p1r/cg_keys_r13w16_16fikpqrstwb.txt \
  bash $N/U86.sh sol_k86GS22_in02 $N/cand/sol_k86GS22_in02.json 1 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json \
  rpatN=$N/rpat/rpatN3_rotation_justified.txt hatbb hbkeys=$N/hatbb/cg_keys_w6b16x_hatbb.txt
