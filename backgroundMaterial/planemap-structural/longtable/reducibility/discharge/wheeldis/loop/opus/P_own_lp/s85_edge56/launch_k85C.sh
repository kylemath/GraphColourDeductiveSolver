# s85: k85C / k85CL = k85B / k85L with W6 round-11 cg_keys_124.txt (35f58f8f: the 111 keys + cg00_0..12) (swarm request 10:05Z).
# warm = k85B's warm list + k85B's final rows (18,661) + k85L's final rows (4,714) + W6's d = 8 floor receivers (232); in-point = k85B in10
# (upperR2 FEASIBLE 0.020748428855 with the 111 keys; the 13 new keys enter at 0).  k85C: in-out ladder (as k85B), 2 threads; k85CL: lext lextcert, 2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56
export STACK=s77 ARGS=$S79/args_A97_F.txt XF=c6le KEYS=$Z/keys/cg_keys_124.txt
export WARM=$(cat $Z/runK_k85B/warmlist.txt),$Z/runK_k85B/rows_k85B_final.txt,$Z/runK_k85L/rows_k85L_final.txt,$Z/w6d8/inject_rows.txt
export FEAS=$Z/cand/sol_k85B_in10.json
nohup bash $Z/runK85.sh 200 2 k85C inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $Z/logs/runK_k85C.out 2>&1 &
sleep 2
nohup bash $Z/runK85.sh 200 2 k85CL lext lextcert q7pen=1e-3 > $Z/logs/runK_k85CL.out 2>&1 &
