# s86: k86FL on W13+K3c (args_A97_F_W13K3c.txt 27de70e4, all 8 K-3 kills, Lean done Studio 2d7ba139) + FINAL A-5 rule file rules/A5final/rules_c67fa1d1_plus_A5_twins.json (2db75746, 6,718 = c67fa1d1 + all 274 re-justified; [E2] Studio ST-18 main 92c8a166) + rpatN 8b90a842 + 151 keys + c6le. Warm adds k86CS rows through its it-1 separation.
# + f2b7 rules c67fa1d1 [E2] + rpatN 8b90a842 [E2] + 151 keys + c6le.  Replaces k86ML.  warm = k86U list + k86L rows through its it-4 separation.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3c.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt,$N/warm/rows_k86CS_snap_it1.txt
nohup bash $N/runK86.sh 200 2 k86FL lext lextcert q7pen=1e-3 > $N/logs/runK_k86FL.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86FL > $N/logs/watchL86_k86FL.out 2>&1 &
