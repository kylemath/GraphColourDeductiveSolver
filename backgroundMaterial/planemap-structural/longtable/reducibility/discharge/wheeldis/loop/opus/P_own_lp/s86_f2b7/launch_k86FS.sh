# s86: k86FS on W13+K3c (args_A97_F_W13K3c.txt 27de70e4, all 8 K-3 kills, Lean done Studio 2d7ba139) + FINAL A-5 rule file rules/A5final/rules_c67fa1d1_plus_A5_twins.json (2db75746, 6,718 = c67fa1d1 + all 274 re-justified; [E2] Studio ST-18 main 92c8a166) + rpatN 8b90a842 + 151 keys + c6le. Warm adds k86CS rows through its it-1 separation.
# + pat=w13/pat_K3_D.out e72617ed: f8_.56.5656_56...55., f9_...575655_...5..65.; swarm K-3 [P-D], Studio K3CHK main a6c989e5 second engine)
# + f2b7 rules c67fa1d1 [E2] + rpatN 8b90a842 [E2] + cg_keys_r13.txt (151 keys) + c6le.  Replaces k86KS.  In-point $1 must pass upperR2
# under exactly this family (logs/upper_K_<point>.log).  warm = k86B warm list + its rows at it 13.  2 threads.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56; N=$B/s86_f2b7
export STACK=s77 ARGS=$N/args_A97_F_W13K3c.txt XF="c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt" KEYS=$Z/keys/cg_keys_r13.txt FEAS=$N/cand/$1.json
P1=${1#sol_}; grep -q "^UPPER-R2: FEASIBLE" $N/logs/upper_F_$P1.log || { echo "in-point $1 has no FEASIBLE recheck under the proof-stack family" >&2; exit 2; }
export WARM=$(cat $N/runK_k86B/warmlist.txt),$N/warm/rows_k86B_snap_it13.txt,$N/warm/rows_k86CS_snap_it1.txt
nohup bash $N/runK86.sh 200 2 k86FS inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall > $N/logs/runK_k86FS.out 2>&1 &
sleep 5
cd $N && nohup bash $N/watch86.sh k86FS > $N/logs/watch86_k86FS.out 2>&1 &
cd $N && nohup bash $N/file86.sh k86FS > $N/logs/file86_k86FS.out 2>&1 &
