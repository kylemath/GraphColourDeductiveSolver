#!/bin/bash
# B3 sequential driver v3 (1 core, nice 15): waits for the Q screener, then K, L8, F, PT (rings <= 13), then ring 14
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sB3_kills
while kill -0 25490 2>/dev/null; do sleep 20; done
nice -n 15 python3 scripts/scrB3.py results/res_K.tsv 13 windows/famK_T1_R13.tsv flist_K.tags > logs/scr_K.log 2>&1
nice -n 15 python3 scripts/scrB3.py results/res_L8.tsv 13 windows/famL8_g5_R14.tsv flist_L8.tags > logs/scr_L8.log 2>&1
MINSC=12:2,13:2 nice -n 15 python3 scripts/scrB3.py results/res_T1F.tsv 13 windows/famT1_R14.tsv flist_T1_F.tags > logs/scr_T1F.log 2>&1
nice -n 15 python3 scripts/scrB3.py results/res_T1PT.tsv 13 windows/famT1_R14.tsv flist_T1_PT.tags > logs/scr_T1PT.log 2>&1
echo STAGES13_DONE >> logs/scr_T1PT.log
nice -n 15 python3 scripts/scrB3.py results/res_T1s1b.tsv 14 windows/famT1_R14.tsv flist_T1_stage1.tags > logs/scr_T1s1b.log 2>&1
MINSC=12:2,13:2,14:3 nice -n 15 python3 scripts/scrB3.py results/res_T1F14.tsv 14 windows/famT1_R14.tsv flist_T1_F.tags > logs/scr_T1F14.log 2>&1
echo STAGES_DONE >> logs/scr_T1F14.log
