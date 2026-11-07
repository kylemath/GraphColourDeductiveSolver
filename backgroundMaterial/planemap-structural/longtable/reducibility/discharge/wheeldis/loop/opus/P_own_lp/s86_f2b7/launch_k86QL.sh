# s86: k86QL = lext lextcert pure-t lower on the proof-stack family: W13 stack (args_A97_F_W13.txt 5faa1ad6) + f2b7 with
# rules/rules_studio_keep95p131f_W18strict.json (c67fa1d1, 6,444 rules = 2b362955 + 428 W18-justified, [E2] with Studio ST-12 main 8559d561)
# + rpatN=rpat/rpatN3_rotation_justified.txt (8b90a842, [E2]) + cg_keys_r13.txt (151 keys).  Replaces k86PL.  warm = k86U list + k86L rows
# through its it-4 separation.  2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_studio_keep95p131f_W18strict.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86QL lext lextcert q7pen=1e-3 > $N/logs/runK_k86QL.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86QL > $N/logs/watchL86_k86QL.out 2>&1 &
