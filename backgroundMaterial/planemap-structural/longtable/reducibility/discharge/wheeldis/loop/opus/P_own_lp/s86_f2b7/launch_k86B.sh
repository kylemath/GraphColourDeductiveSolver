# s86: k86B = k86A with cg_keys_r12.txt (bb547900: cg_keys_124 + the 16 keys W6 r12 priced as improving on the k85CL phase-1 dual,
# swarm round6/W6-rule-grammar/round12/opus_k85CL_price.json); f2b7 on; same warm list and in-point (k85C in03; the 16 new keys enter at 0).
# k86L = lext lextcert on the same family (f2b7 + 140 keys), warm = k85CL's warm list + k85CL's rows (the 0.000689 cert's row source) + k85C it3 rows.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$S79/args_A97_F.txt XF="c6le f2b7" KEYS=$Z/keys/cg_keys_r12.txt
export FEAS=$N/cand/sol_k85C_in03.json
WARMA=$(cat $Z/runK_k85C/warmlist.txt),$N/warm/rows_k85C_snap_it3.txt,$N/warm/rows_k85CL_snap_it1.txt
WARML=$(cat $Z/runK_k85CL/warmlist.txt),$N/warm/rows_k85CL_snap_it1.txt,$N/warm/rows_k85C_snap_it3.txt
WARM=$WARMA nohup bash $N/runK86.sh 200 2 k86B inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86B.out 2>&1 &
sleep 2
WARM=$WARML nohup bash $N/runK86.sh 200 2 k86L lext lextcert q7pen=1e-3 > $N/logs/runK_k86L.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86B > $N/logs/watch86_k86B.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86B > $N/logs/file86_k86B.out 2>&1 &
cd $N && nohup bash $N/watchL86.sh k86L > $N/logs/watchL86_k86L.out 2>&1 &
