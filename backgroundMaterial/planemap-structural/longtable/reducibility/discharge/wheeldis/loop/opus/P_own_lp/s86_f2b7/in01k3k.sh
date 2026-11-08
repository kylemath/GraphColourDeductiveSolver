# s86: our own K3k check of sol_k86GS3b_in01 (Studio ST-41 control A says it is FEASIBLE on K3k too); memory-gated.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; B=$(dirname $N)
while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 4500 ]; do sleep 20; done
export STACK=s77 ARGS=$N/args_A97_F_W13K3k.txt KEYS=$B/s85_edge56/keys/cg_keys_r13w16.txt
bash $N/U86.sh F_k86GS3b_in01_K3k $N/cand/sol_k86GS3b_in01.json 1 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt vK=1000000 vfile=$N/logs/viol_F_k86GS3b_in01_K3k.txt
