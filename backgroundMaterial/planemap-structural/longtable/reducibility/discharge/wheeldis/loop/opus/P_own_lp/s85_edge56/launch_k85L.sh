# s85: k85L = lexicographic pure-t K run (swarm request 05:45Z) next to the penalised k85B: phase 1 min t alone on the current rows (t1, a valid
# lower estimate that can only rise), phase 2 the K costs (keeppen xpen=1e-3, q7pen=1e-3) at t <= t1 + 1e-9, raw separation at the phase-2 point
# (no in-out); lextcert writes the phase-1 cert when t1 > 0.  Same stack/keys/flags as k85B; warm = k85B warm list + its iter-4 rows (8,425).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56
export STACK=s77 ARGS=$S79/args_A97_F.txt XF=c6le KEYS=$Z/keys/A97F_111keys.txt
export WARM=$(cat $Z/runK_k85B/warmlist.txt),$Z/runK_k85B/rows_k85B_snap_it4.txt
export FEAS=$Z/cand/sol_k85B_in04.json
nohup bash $Z/runK85.sh 200 1 k85L lext lextcert q7pen=1e-3 > $Z/logs/runK_k85L.out 2>&1 &
