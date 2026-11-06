# s86: k86U = lext lextcert pure-t lower on the k86B / k86L family (f2b7 + cg_keys_r12, 140 keys), warm = the union of both runs' warm
# lists + k86B's rows at iteration 12 + k86L's rows at iteration 4.  Point: k86L separates at t = 0 points only; k86B's rows were cut at
# t ~ 0.013..0.019 points, so the union may already hold t > 0.  1 thread (the two running lanes keep 2 each).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$S79/args_A97_F.txt XF="c6le f2b7" KEYS=$Z/keys/cg_keys_r12.txt FEAS=$N/cand/sol_k86B_in09.json
export WARM=$(cat $N/warm/warmlist_k86U.txt)
nohup bash $N/runK86.sh 200 1 k86U lext lextcert q7pen=1e-3 > $N/logs/runK_k86U.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86.sh k86U > $N/logs/watchL86_k86U.out 2>&1 &
