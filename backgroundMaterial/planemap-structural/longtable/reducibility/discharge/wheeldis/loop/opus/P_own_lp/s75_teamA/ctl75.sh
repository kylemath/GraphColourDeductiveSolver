# s75 Team A in-out controls (copy of s70 ctl70.sh) (dry run, no LP, no warm rows).  usage: bash ctl70.sh <tag> <lam> [rawsol=<json>]   (threads=1, nice 15)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
TAG=$1; LAMC=$2; shift 2; FE=${FE:-$N/sol_feas.json}; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 ${Q7F-q7 q7m q7rc q7cap=3}"; WK=$SC/P/wr75c_$TAG; mkdir -p $WK $N/logs
cd $N/eng
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=ctl_$TAG $A $CB feas=$FE inoutctl=$LAMC xcap=3 xpen=1e-3 threads=1 work=$WK K=300 "$@" > $N/logs/ctl_$TAG.log 2>&1
[ -z "$KEEPWK" ] && rm -rf $WK
