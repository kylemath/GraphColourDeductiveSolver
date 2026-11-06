# s86: k86M = lext lextcert pure-t lower on f2b7 + cg_keys_r13.txt (fe8a97a7, 151 keys = r12 + W6's 11 payer-7 keys; gkwintest151 and
# gkself151 PASS).  Why now: k86L's it-5 phase-1 cert (t1 = 0.000421, f2b7 + 140 keys) prices all 11 new keys as improving
# (dualexport on r13: cg12_76_0 colsum +0.048, 77_* +0.0052, 78_* +0.0033, 75_0 +0.0017, 79_* ~1e-5), so it does not bound the
# 151-key family.  warm = k86U's warm list (k86B + k86L union) + k86L's rows through its it-4 separation (the rows of that cert).
# Stack: args_A97_F_W13.txt (5faa1ad6) = args_A97_F.txt + W13's 115 kill patterns (27 D, 88 C; w13/MD5SUMS); the k86L cert loses 62
# receivers (20.6% of its d = 7 receiver |w|) to them, so its 0.000421 does not bound this stack either.
# Replaces k86U (stopped after its it-0 phase 1); 1 thread.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k86B_in10.json
[ -e $N/warm/rows_k86L_snap_it5.txt ] || cp $N/eng/rows_k86L.txt $N/warm/rows_k86L_snap_it5.txt
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 1 k86M lext lextcert q7pen=1e-3 > $N/logs/runK_k86M.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86.sh k86M > $N/logs/watchL86_k86M.out 2>&1 &
