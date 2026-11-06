# s85: K k85B = full-stack K solve with all 111 W6 keys (A97F_111keys.txt a5dfd233) (gkwin gkleaf c6le) from k79L in01 with K* as key KS (sol_k79L_in01_gk.json,
# FEASIBLE on s85 at 0.022450440897, 02:19Z); warm = k83F's list (k83F stopped: superseded)
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s78_kstar; S79=$B/s79_routeF; P=$B/s83_cons6; Z=$B/s85_edge56
export STACK=s77 ARGS=$S79/args_A97_F.txt XF=c6le KEYS=$Z/keys/A97F_111keys.txt
export FAM=full KS=0; . $Z/env85.sh
export WARM=$W7POOL,$WX75,$WK75,$N/warm/rows_q75B_snap78.txt,$N/warm/rows_b77F_snap78.txt,$N/tests/t6/pool_W6support_floor.txt,$N/tests/t6/pool_b77U6dual_floor.txt,$S79/rows_b77F_final.txt,$S79/rows_q75B_snap4.txt,$P/warm/rows_k79K_snap83.txt,$N/warm/rows_k79K_final_restart.txt,$P/warm/rows_k83C_restart.txt,$P/warm/rows_k83D_restart.txt,$P/warm/rows_k79L_restart.txt
export FEAS=$Z/tests/sol_k79L_in01_gk.json
nohup bash $Z/runK85.sh 200 2 k85B inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $Z/logs/runK_k85B.out 2>&1 &
