# s86: k86GL5 = k86GL4 + W6b-16i keys (20, cg_keys_w6b16i 575d59c9, priced on the k86GL4 p1_00 dual). k86GL4 was: the k86GL3 lower family (lext on K3g args bef43766 + rules 2db75746 + rpatN3 + offc_K3g_2f4f0f02 + c6le + f2b7, consk=20)
# + flag p1r (KEYSPEC v2 single-row receiver key coefficients on d = 7 / 8 rows, W6b KEYSPEC2_RECEIVER.md d5a6734b section 3.3;
# p1r/README.md) on the engine copy s86_f2b7/eng_p1r (runner / watchers: p1r/runK86p.sh, p1r/watchL86p.sh, p1r/dualwatch86p.sh).
# Keys: $KEYS4, default p1r/cg_keys_r13w16_16f.txt (r13w16 171 + W6b-16f cur 19 + v2 10 = 200 keys; 77 payer-7 keys, so the d = 7 leaf
# uses eng_p1r/bin/jsepf_gk_k192).  Warm = k86GL3's list, plus k86GL3's own rows (snapshot copied to warm/ at launch) if that file is non-empty.
# Start only after k86GL4 has stopped (memory: two LP runs at most); gl5gate.sh does that after GL4 iteration 0.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
[ -x $N/eng_p1r/bin/jsepf_gk_k192 ] || { echo "launch_k86GL5: eng_p1r/bin/jsepf_gk_k192 missing; build: cd $N/eng_p1r && c++ -O3 -march=native -std=c++17 -pthread -o bin/jsepf_gk_k192 jsepf_gk_k192.cpp" >&2; exit 2; }
export STACK=s77 ARGS=$N/args_A97_F_W13K3g.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r" KEYS=${KEYS5:-$N/p1r/cg_keys_r13w16_16fi.txt} FEAS=$N/cand/sol_k85C_in03.json
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt,$N/warm/rows_k86CS_snap_it1.txt,$N/warm/rows_k86FL_snap_it1.txt,$N/warm/rows_k86GL_snap_it2.txt,$N/warm/rows_k86GL2_snap_it2.txt
WARM=$WARM,$N/warm/rows_k86GL3_snap_GL4.txt; if [ -s $N/eng_p1r/rows_k86GL4.txt ]; then cp $N/eng_p1r/rows_k86GL4.txt $N/warm/rows_k86GL4_snap_GL5.txt; WARM=$WARM,$N/warm/rows_k86GL4_snap_GL5.txt; fi
nohup bash $N/p1r/runK86p.sh 200 2 k86GL5 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 > $N/logs/runK_k86GL5.out 2>&1 &
sleep 5
cd $N && nohup bash $N/p1r/watchL86p.sh k86GL5 > $N/logs/watchL86_k86GL5.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/p1r/dualwatch86p.sh k86GL5 > $N/logs/dualwatch86_k86GL5.out 2>&1 &
