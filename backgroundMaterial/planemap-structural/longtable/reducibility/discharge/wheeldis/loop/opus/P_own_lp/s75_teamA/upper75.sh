# s75 Team A: upperR2 exhaustive (d=7..17 + Karp tail) on a sol json, extended stack flags (hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3).  usage: bash upper75.sh <tag> <sol json> [threads] [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; WK=$SC/P/wr75u_$TAG; mkdir -p $WK; cd $N/eng
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=$TH work=$WK "$@" > $N/logs/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s75U-$TAG] $SOL: $(grep 'UPPER-R2' $N/logs/upper_$TAG.log | tail -1)" >> $N/run.log
[ -z "$KEEPWK" ] && rm -rf $WK   # s75: work dirs are ~200 MB each; disk is short
