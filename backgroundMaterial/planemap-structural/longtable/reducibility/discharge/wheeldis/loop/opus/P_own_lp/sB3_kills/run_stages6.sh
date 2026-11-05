#!/bin/bash
# B3 driver v6 (1 core, nice 15; bounded): waits for the CB ring-14 stage (PID 7372), then targets_v2 rows at ring 13,
# then ring 14 for the B mate 5757577/5577567 (Q and P families), then exits.
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sB3_kills
while kill -0 7372 2>/dev/null; do sleep 20; done
echo CB14_DONE >> logs/scr_CB14.log
MINSC=12:2,13:2 nice -n 15 python3 scripts/scrB3.py results/res_V2_13.tsv 13 windows/famV2_R14.tsv flist_V2.tags > logs/scr_V2_13.log 2>&1
echo V2_13_DONE >> logs/scr_V2_13.log
MINSC=12:2,13:2,14:2 nice -n 15 python3 scripts/scrB3.py results/res_r3b14.tsv 14 windows/famV2_R14.tsv flist_r3b.tags > logs/scr_r3b14.log 2>&1
echo R3B14_DONE >> logs/scr_r3b14.log
