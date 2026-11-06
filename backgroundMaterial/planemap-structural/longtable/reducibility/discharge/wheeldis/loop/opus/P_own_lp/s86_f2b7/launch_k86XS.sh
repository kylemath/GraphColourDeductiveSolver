# s86: k86XS = in-out K upper ladder on the rot family: W13 stack (args_A97_F_W13.txt 5faa1ad6) + f2b7 with the Studio's
# rotation-preserving DERIVE file rules/rules_zcons_rot.json (079673b0, 5,974 rules = 2b362955 minus 42; subset of every audited file, so
# its uppers hold for each) + cg_keys_r13.txt (151 keys).  In-point $1 = a point that passed upperR2 under exactly this family
# (logs/upper_X_<point>.log), e.g. sol_q53A97q (0.098789, f2b-free).  warm = k86B warm list + its rows at it 13.  2 threads.  Replaces k86RS.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_zcons_rot.json" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/$1.json
grep -q "^UPPER-R2: FEASIBLE" $N/logs/upper_X_${1#sol_}.log || { echo "in-point $1 has no FEASIBLE recheck under the rot family (079673b0)" >&2; exit 2; }
export WARM=$(cat $N/runK_k86B/warmlist.txt),$N/warm/rows_k86B_snap_it13.txt
nohup bash $N/runK86.sh 200 2 k86XS inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86XS.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86XS > $N/logs/watch86_k86XS.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86XS > $N/logs/file86_k86XS.out 2>&1 &
