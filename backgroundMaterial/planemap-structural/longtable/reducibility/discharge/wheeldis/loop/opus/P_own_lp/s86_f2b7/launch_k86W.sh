# s86: k86W = in-out K upper ladder (as k86B) on the W13 stack: args_A97_F_W13.txt (5faa1ad6; A97 + patched298 + route F + W13's 115 kill
# patterns, 27 D + 88 C, all two-engine and in Lean) with f2b7 + cg_keys_r13.txt (151 keys).  In-point k86B in10 (t = 0.018311138,
# upperR2 FEASIBLE on the smaller family: more kills and extra keys at 0 keep it feasible).  warm = k86B's warm list + k86B's rows at it 13.
# Replaces k86L (stopped after its positive it-5 phase 1); 2 threads.  Points file to from_opus/s86_k86W/ after upperR2 on this stack.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k86B_in10.json
export WARM=$(cat $N/runK_k86B/warmlist.txt),$N/warm/rows_k86B_snap_it13.txt
nohup bash $N/runK86.sh 200 2 k86W inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86W.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86W > $N/logs/watch86_k86W.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86W > $N/logs/file86_k86W.out 2>&1 &
