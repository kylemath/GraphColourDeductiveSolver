#!/bin/bash
# B3 sequential driver v2 (1 core, nice 15): rings <= 13 everywhere first, ring 14 last
cd /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/sB3_kills
nice -n 15 python3 scripts/scrB3.py results/res_Q.tsv 13 windows/famQ_R13.tsv flist_Q.tags > logs/scr_Q.log 2>&1
nice -n 15 python3 scripts/scrB3.py results/res_L8.tsv 13 windows/famL8_g5_R14.tsv flist_L8.tags > logs/scr_L8.log 2>&1
MINSC=12:2,13:2 nice -n 15 python3 scripts/scrB3.py results/res_T1F.tsv 13 windows/famT1_R14.tsv flist_T1_F.tags > logs/scr_T1F.log 2>&1
nice -n 15 python3 scripts/scrB3.py results/res_T1PT.tsv 13 windows/famT1_R14.tsv flist_T1_PT.tags > logs/scr_T1PT.log 2>&1
echo STAGES13_DONE >> logs/scr_T1PT.log
nice -n 15 python3 scripts/scrB3.py results/res_T1s1b.tsv 14 windows/famT1_R14.tsv flist_T1_stage1.tags > logs/scr_T1s1b.log 2>&1
MINSC=12:2,13:2,14:3 nice -n 15 python3 scripts/scrB3.py results/res_T1F14.tsv 14 windows/famT1_R14.tsv flist_T1_F.tags > logs/scr_T1F14.log 2>&1
echo STAGES_DONE >> logs/scr_T1F14.log
