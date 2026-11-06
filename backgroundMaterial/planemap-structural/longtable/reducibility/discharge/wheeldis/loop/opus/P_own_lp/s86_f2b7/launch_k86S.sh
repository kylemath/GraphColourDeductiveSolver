# s86: k86S = sound in-out K upper ladder (as k86B) on the OP-11 family: W13 stack (args_A97_F_W13.txt) + f2b7 with the filtered rules
# (rules/rules_studio_keep95p131f_f7s.json, 704c371f) + cg_keys_r13.txt (151 keys).  In-point $1 = a k86B point that passed upperR2
# under exactly this family (logs/upper_W13s_<point>.log).  warm = k86B's warm list + its rows at it 13.  2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; S79=$B/s79_routeF; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_studio_keep95p131f_f7s.json" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/$1.json
grep -q "^UPPER-R2: FEASIBLE" $N/logs/upper_W13s_${1#sol_}.log || { echo "in-point $1 has no FEASIBLE recheck under the W13s family" >&2; exit 2; }
export WARM=$(cat $N/runK_k86B/warmlist.txt),$N/warm/rows_k86B_snap_it13.txt
nohup bash $N/runK86.sh 200 2 k86S inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86S.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86S > $N/logs/watch86_k86S.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86S > $N/logs/file86_k86S.out 2>&1 &
