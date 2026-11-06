# s86: k86V = k86L continued with a different separation point (k86L stopped after its it-5 phase 1; BINDING.md 21:00Z: at the lext
# phase-2 vertex the free 6-spoke h columns sit at 5.000 and the d >= 9 separation budget (K = 300) goes to cutting them, the same link
# words every round).  Changes: (1) in-out separation (as k86B) between the phase-2 point and the feasible in-point k86B in10
# (t = 0.018311138, upperR2 FEASIBLE); rows violated at a blend are violated at the phase-2 point too, so the lower logic is unchanged;
# (2) hpen=1e-6: a tiny phase-2 cost on h (phase 1, the lower estimate, still minimises t alone).  Family unchanged: f2b7 + cg_keys_r12.
# warm = k86L's warm list + k86L's rows (through its it-4 separation).  2 threads (k86L's).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$S79/args_A97_F.txt XF="c6le f2b7" KEYS=$Z/keys/cg_keys_r12.txt FEAS=$N/cand/sol_k86B_in10.json
cp $N/eng/rows_k86L.txt $N/warm/rows_k86L_snap_it5.txt
export WARM=$(cat $N/runK_k86L/warmlist.txt),$N/warm/rows_k86L_snap_it5.txt
nohup bash $N/runK86.sh 200 2 k86V lext lextcert q7pen=1e-3 hpen=1e-6 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 feascols feasall > $N/logs/runK_k86V.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watchL86.sh k86V > $N/logs/watchL86_k86V.out 2>&1 &
cd $N && nohup bash $N/watch86.sh k86V > $N/logs/watch86_k86V.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86V > $N/logs/file86_k86V.out 2>&1 &
