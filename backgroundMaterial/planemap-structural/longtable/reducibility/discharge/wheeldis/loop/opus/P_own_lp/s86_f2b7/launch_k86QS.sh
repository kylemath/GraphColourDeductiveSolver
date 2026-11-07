# s86: k86QS = in-out K upper ladder on the proof-stack family: W13 stack (args_A97_F_W13.txt 5faa1ad6) + f2b7 with
# rules/rules_studio_keep95p131f_W18strict.json (c67fa1d1, 6,444 rules, [E2]) + rpatN=rpat/rpatN3_rotation_justified.txt (8b90a842, [E2])
# + cg_keys_r13.txt (151 keys).  Replaces k86PS.  In-point $1 must pass upperR2 under exactly this family
# (logs/upper_Q_<point>.log), e.g. sol_q66_q (s33z/run_A67 0.128958, l3q only: no f2b, no rpatN).  warm = k86B warm list + its rows at
# it 13.  2 threads.  Replaces k86XS (killed in setup by the container restart; its in-point q53A97q fails without the 46).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13.txt XF="c6le f2b7 f2b=$N/rules/rules_studio_keep95p131f_W18strict.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/$1.json
P1=${1#sol_}; grep -q "^UPPER-R2: FEASIBLE" $N/logs/upper_Q_$P1.log || { echo "in-point $1 has no FEASIBLE recheck under the proof-stack family" >&2; exit 2; }
export WARM=$(cat $N/runK_k86B/warmlist.txt),$N/warm/rows_k86B_snap_it13.txt
nohup bash $N/runK86.sh 200 2 k86QS inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86QS.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86QS > $N/logs/watch86_k86QS.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86QS > $N/logs/file86_k86QS.out 2>&1 &
