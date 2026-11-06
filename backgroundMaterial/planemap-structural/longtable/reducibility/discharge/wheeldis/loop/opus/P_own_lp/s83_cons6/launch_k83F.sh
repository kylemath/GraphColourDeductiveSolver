# s83: K k83F = k83F restarted after the 01:30Z container restart, from k79L in01 (0.0224504, FEASIBLE equality -> c6le); warm += k83F + k79L rows
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s78_kstar; S79=$B/s79_routeF; P=$B/s83_cons6
export STACK=s77 ARGS=$S79/args_A97_F.txt FAM=full KS=1 EGK=$N/eng/edgekeys_r4.txt XF=c6le
. $P/env83.sh
export WARM=$W7POOL,$WX75,$WK75,$N/warm/rows_q75B_snap78.txt,$N/warm/rows_b77F_snap78.txt,$N/tests/t6/pool_W6support_floor.txt,$N/tests/t6/pool_b77U6dual_floor.txt,$S79/rows_b77F_final.txt,$S79/rows_q75B_snap4.txt,$P/warm/rows_k79K_snap83.txt,$N/warm/rows_k79K_final_restart.txt,$P/warm/rows_k83C_restart.txt,$P/warm/rows_k83D_restart.txt,$P/warm/rows_k79L_restart.txt
export FEAS=$N/cand/sol_k79L_in01.json
nohup bash $P/runK83.sh 200 2 k83F inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $P/logs/runK_k83F.out 2>&1 &
sleep 20; nohup bash $P/watch83.sh k83F > $P/logs/watch_k83F.out 2>&1 &
