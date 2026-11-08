# s86: memory-gated upperR2 of one candidate at its own t on a named family.  usage: bash chkfam.sh <cand/sol_X.json> <K3k|K3l|...>
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7; B=$(dirname $N)
SOL=$(readlink -f $1); FAMN=$2; X=$(basename $SOL .json); X=${X#sol_}
while [ $(awk '/MemAvailable/{print int($2/1024)}' /proc/meminfo) -lt 4500 ]; do sleep 20; done
export STACK=s77 ARGS=$N/args_A97_F_W13${FAMN}.txt KEYS=$B/s85_edge56/keys/cg_keys_r13w16.txt
[ -s $ARGS ] || { echo "no args file $ARGS" >&2; exit 2; }
bash $N/U86.sh F_${X}_${FAMN} $SOL 1 c6le f2b7 f2b=$N/rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=$N/rpat/rpatN3_rotation_justified.txt vK=1000000 vfile=$N/logs/viol_F_${X}_${FAMN}.txt
