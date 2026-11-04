# usage: bash upper69.sh <tag> <sol> [extra flags]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s69_rrzq7/env69.sh
TAG=$1; SOL=$2; shift 2; F="$FUP f2b=$RULES hatrr zh zr zcap=3"; mkdir -p $N/work_$TAG; cd $N/eng
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=2 work=$N/work_$TAG "$@" > $N/logs/upper_$TAG.log 2>&1
