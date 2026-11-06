# s86: k86ZL = lext lextcert pure-t lower on the zcons family: W13 stack (args_A97_F_W13.txt 5faa1ad6) + f2b7 with the Studio's
# Z-consistent rule file rules/rules_zcons.json (e6c496a1 = 45a4c6d1 minus the 3,036 rules whose requirement sets contradict the
# structure Z; Studio main a7fbd198) + cg_keys_r13.txt (151 keys).  Replaces k86T (f7s, stopped before it 1).  warm = k86U's warm
# list (k86B + k86L union) + k86L's rows through its it-4 separation.  2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_zcons.json" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86ZL lext lextcert q7pen=1e-3 > $N/logs/runK_k86ZL.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86ZL > $N/logs/watchL86_k86ZL.out 2>&1 &
