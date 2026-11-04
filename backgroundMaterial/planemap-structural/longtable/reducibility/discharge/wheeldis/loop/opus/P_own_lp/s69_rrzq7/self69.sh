# usage: bash self69.sh <tag> <sol> <N> [flags]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s69_rrzq7/env69.sh
TAG=$1; SOL=$2; NS=$3; shift 3; F="$FUP f2b=$RULES hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; mkdir -p $N/work_$TAG; cd $N/eng
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=2 work=$N/work_$TAG f2bself=$NS "$@" > $N/logs/upper_$TAG.log 2>&1
