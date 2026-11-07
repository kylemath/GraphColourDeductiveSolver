# s86: k86PL = lext lextcert pure-t lower on the proof-stack family: W13 stack (args_A97_F_W13.txt 5faa1ad6) + f2b7 with
# rules/rules_zcons_minus_W18rejects.json (2b362955) + rpatN=rpat/rpatN3_rotation_justified.txt (8b90a842: rpatN3 minus the 46 patterns
# with no rotation-reading witness, OP-16) + cg_keys_r13.txt (151 keys).  Replaces k86RL (killed in setup by the container restart).
# warm = k86U list (k86B + k86L union) + k86L rows through its it-4 separation.  2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_zcons_minus_W18rejects.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86PL lext lextcert q7pen=1e-3 > $N/logs/runK_k86PL.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86PL > $N/logs/watchL86_k86PL.out 2>&1 &
