# usage: bash upper0.sh <engdir> <tag> [extra flags] ; upperR2 on the s64 solc solution (control a/b)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s67_q7/env67.sh
ED=$1; TAG=$2; shift 2; F="$FUP f2b=$RULES"; mkdir -p $N/work_$TAG; cd $ED
SOL=${SOL:-$B/s64_keep95p131f/val/sol_c_repaired_opusfmt.json}
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$N/work_$TAG "$@" > $N/logs/upper_$TAG.log 2>&1
