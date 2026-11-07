# s86: k86GL3 = k86GL2 + off-centre kills (rpatN += offc/offc_K3g_2f4f0f02.txt: 250 rotation-filtered off-centre patterns of the K3g registry, OFFC_SPEC from_opus/offc) + consk=20. Warm adds k86GL2 rows to it 2 (rows the new patterns kill are dropped by admissible()). k86GL2 = lext lower on K3g + keys r13w16.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3g.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt" KEYS=$Z/keys/cg_keys_r13w16.txt FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt,$N/warm/rows_k86CS_snap_it1.txt,$N/warm/rows_k86FL_snap_it1.txt,$N/warm/rows_k86GL_snap_it2.txt,$N/warm/rows_k86GL2_snap_it2.txt
nohup bash $N/runK86.sh 200 2 k86GL3 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 > $N/logs/runK_k86GL3.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86s.sh k86GL3 > $N/logs/watchL86_k86GL3.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/dualwatch86.sh k86GL3 > $N/logs/dualwatch86_k86GL3.out 2>&1 &
