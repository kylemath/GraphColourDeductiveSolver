# s86: k86GL2 = lext lower on the k86GL stack (W13+K3g args bef43766 + 2db75746 + rpatN 8b90a842 + c6le) with keys r13 + W6b-16 (cg_keys_r13w16.txt 15c361a1 = 151 r13 + 20 payer-5/6/7 keys priced on the k86GL p1_00 dual; payer-8/9 file NOT loaded). Replaces k86GL. Warm adds k86GL rows through its it-2 separation.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3g.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13w16.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt,$N/warm/rows_k86CS_snap_it1.txt,$N/warm/rows_k86FL_snap_it1.txt,$N/warm/rows_k86GL_snap_it2.txt
nohup bash $N/runK86.sh 200 2 k86GL2 lext lextcert q7pen=1e-3 > $N/logs/runK_k86GL2.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86GL2 > $N/logs/watchL86_k86GL2.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/dualwatch86.sh k86GL2 > $N/logs/dualwatch86_k86GL2.out 2>&1 &
