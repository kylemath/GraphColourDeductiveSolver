#!/bin/bash
# B3: ring-14/15 whole-row windows for B's mates and the C row, run while the v5 driver (process group 4605) is paused
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sB3_kills
DONLY=1 TO=1500 nice -n 15 python3 scripts/scrB3.py results/res_X15.tsv 15 windows/famX15.tsv flist_X15.tags > logs/scr_X15.log 2>&1
echo X15_DONE >> logs/scr_X15.log
kill -CONT -4605
