# s86: k86ML = lext lextcert pure-t lower on the proof-stack family + all 6 K-3 kills (2 D in pat_K3_D.out + 3 D in pat_K3b_D.out a0b171e2 + 1 C X={I5-I6} in pat_K3b_C.cfast ff6a66bd; Studio K3CHK2 main cfcd6497) (args_A97_F_W13K3.txt 58b48b54, see launch_k86KS.sh)
# + f2b7 rules c67fa1d1 [E2] + rpatN 8b90a842 [E2] + 151 keys + c6le.  Replaces k86KL.  warm = k86U list + k86L rows through its it-4 separation.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3b.txt XF="c6le f2b7 f2b=$N/rules/rules_studio_keep95p131f_W18strict.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86ML lext lextcert q7pen=1e-3 > $N/logs/runK_k86ML.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86ML > $N/logs/watchL86_k86ML.out 2>&1 &
