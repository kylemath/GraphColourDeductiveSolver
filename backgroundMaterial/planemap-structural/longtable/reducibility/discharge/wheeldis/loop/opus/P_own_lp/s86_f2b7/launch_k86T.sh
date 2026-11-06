# s86: k86T = lext lextcert pure-t lower on the sound f2b7 family: W13 stack (args_A97_F_W13.txt 5faa1ad6) + f2b7 with the filtered rule
# file rules/rules_studio_keep95p131f_f7s.json (704c371f = 45a4c6d1 minus the 84 d7_w7 + 27 d8_w7 rules per side, and mirrors, that the
# OP-5 review could not justify) + cg_keys_r13.txt (151 keys).  Replaces k86M (never started).  warm = k86U's warm list (k86B + k86L union)
# + k86L's rows through its it-4 separation.  2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_studio_keep95p131f_f7s.json" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86T lext lextcert q7pen=1e-3 > $N/logs/runK_k86T.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86T > $N/logs/watchL86_k86T.out 2>&1 &
