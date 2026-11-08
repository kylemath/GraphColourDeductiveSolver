# s86: k86GV1 = the first KEYSPEC v2 lower lane: k86GL6's family on args K3gB5b (args_A97_F_W13K3gB5b.txt md5 5e399535 = K3gB + K5H01 + K5b
# L1-L3 / U1-U2, all [E2]; coordinator 8 Nov) with flag v2r on the
# engine copy s86_f2b7/eng_v2 (v2r/README.md, v2r/V2ROW_SPEC.md): every d = 7 / 8 receiver is the KEYSPEC v2 max-row (W6b KEYSPEC2_RECEIVER.md
# d5a6734b 3.1), added lazily as realisation rows ('receiverV2', d, link, apex, rho) by an exact max-plus DP; no masked d = 7 / 8 receiver
# row is ever built.  Everything else (d >= 9 receivers with gkwin, senders, cons2, mrows, separators) as k86GL6.  p1r stays in XF as in
# GL6 (it only touches the masked d = 7 / 8 rows, which v2r never builds).
# Keys p1r/cg_keys_r13w16_16fik.txt (3d996dbb, 240; 89 payer-7 keys -> eng_v2/bin/jsepf_gk_k192).  Warm = k86GL6's list (+ k86GL5 / k86GL6
# own rows if non-empty at launch); the warm d = 7 / 8 receivers get their DP argmax row at the seed point v2seed (k86GL5 phase-1 sol,
# snapshot copied to v2r/ at launch).  v2rescan=1: every round the DP re-checks every known d = 7 / 8 receiver (separator top-K crowding).
# v2inner=$V2INNER (default 4; V2INNER=0 gives exactly GL6 flags + v2r): after each phase-1 solve up to 4 rounds of DP on all known d = 7 / 8
# receivers + cold phase-1 re-solve, so the realisation rows settle in fewer lext iterations (the GL5-cert restricted LP needed 17 rounds
# from the seed rows); tested on a small warm set only (v2r/NOTES.md smoke 2).
# Memory: ~5 GB like GL6 plus the realisation rows; start only when at most one other LP run is live and MemAvailable >= 6 GB.
# NOT started by the v2r build; the coordinator starts it.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
[ -x $N/eng_v2/bin/jsepf_gk_k192 ] || { echo "launch_k86GV1: eng_v2/bin/jsepf_gk_k192 missing; build: cd $N/eng_v2 && c++ -O3 -march=native -std=c++17 -pthread -o bin/jsepf_gk_k192 jsepf_gk_k192.cpp" >&2; exit 2; }
[ -s $N/v2r/seed_sol_k86GL5_p1.json ] || cp $N/eng_p1r/sol_k86GL5_p1.json $N/v2r/seed_sol_k86GL5_p1.json
export STACK=s77 ARGS=${ARGSV:-$N/args_A97_F_W13K3gB5b.txt} KEYS=${KEYSV:-$N/p1r/cg_keys_r13w16_16fik.txt} FEAS=$N/cand/sol_k85C_in03.json
export XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt,$N/offc/offc_K3g_2f4f0f02.txt p1r v2r v2seed=$N/v2r/seed_sol_k86GL5_p1.json v2rescan=1 v2inner=${V2INNER:-4}"
export WARM=$(cat $N/runK_k86U/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt,$N/warm/rows_k86CS_snap_it1.txt,$N/warm/rows_k86FL_snap_it1.txt,$N/warm/rows_k86GL_snap_it2.txt,$N/warm/rows_k86GL2_snap_it2.txt
WARM=$WARM,$N/warm/rows_k86GL3_snap_GL4.txt,$N/warm/rows_k86GL4_snap_GL5.txt
for g in GL5 GL6; do if [ -s $N/eng_p1r/rows_k86$g.txt ]; then cp $N/eng_p1r/rows_k86$g.txt $N/v2r/rows_k86${g}_snap_GV1.txt; WARM=$WARM,$N/v2r/rows_k86${g}_snap_GV1.txt; fi; done
nohup bash $N/v2r/runK86v.sh 200 2 k86GV1 lext lextcert q7pen=1e-3 consk=20 consfrac=0.25 > $N/logs/runK_k86GV1.out 2>&1 &
sleep 5
cd $N && nohup bash $N/v2r/watchL86v.sh k86GV1 > $N/logs/watchL86_k86GV1.out 2>&1 &
cd $N && STACK=$STACK ARGS=$ARGS KEYS=$KEYS XF="$XF" nohup bash $N/v2r/dualwatch86v.sh k86GV1 > $N/logs/dualwatch86_k86GV1.out 2>&1 &
