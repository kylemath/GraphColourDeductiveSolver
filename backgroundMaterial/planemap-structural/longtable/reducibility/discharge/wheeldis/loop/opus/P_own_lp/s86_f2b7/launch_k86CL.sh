# s86: k86CL on W13+K3c (args_A97_F_W13K3c.txt 27de70e4 = W13K3b + pat_K3c_D.out f8c6eb48 [D f9_75..65656_5...55...] + pat_K3c_C.cfast e9ca2a17 [C f9_.56.56555_.5....... X={I0-I5}]; Studio K3CHK3 main 9abebe3b) + rules 363dd708 [E2] + rpatN 8b90a842 + 151 keys + c6le
# + f2b7 rules c67fa1d1 [E2] + rpatN 8b90a842 [E2] + 151 keys + c6le.  Replaces k86ML.  warm = k86U list + k86L rows through its it-4 separation.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3c.txt XF="c6le f2b7 f2b=$N/rules/A5/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86CL lext lextcert q7pen=1e-3 > $N/logs/runK_k86CL.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86CL > $N/logs/watchL86_k86CL.out 2>&1 &
