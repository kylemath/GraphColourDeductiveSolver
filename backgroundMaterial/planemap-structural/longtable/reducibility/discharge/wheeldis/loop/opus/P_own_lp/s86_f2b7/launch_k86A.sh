# s86: k86A = k85C with f2b7 (q7m masks on 7-sides from the f2b d7_w7/d8_w7 rules; spec from_opus/f2b7/SPEC.md), same stack, 124 keys,
# warm = k85C's warm list + k85C's rows (it3 snapshot) + k85CL's rows (it1 snapshot); in-point = k85C in03 (upperR2 FEASIBLE 0.020277318803
# without f2b7; with f2b7 loads only fall).  In-out ladder as k85C, 2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$S79/args_A97_F.txt XF="c6le f2b7" KEYS=$Z/keys/cg_keys_124.txt
export WARM=$(cat $Z/runK_k85C/warmlist.txt),$N/warm/rows_k85C_snap_it3.txt,$N/warm/rows_k85CL_snap_it1.txt
export FEAS=$N/cand/sol_k85C_in03.json
nohup bash $N/runK86.sh 200 2 k86A inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86A.out 2>&1 &
sleep 2
cd $N && nohup bash $N/watch86.sh k86A > $N/logs/watch86_k86A.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86A > $N/logs/file86_k86A.out 2>&1 &
