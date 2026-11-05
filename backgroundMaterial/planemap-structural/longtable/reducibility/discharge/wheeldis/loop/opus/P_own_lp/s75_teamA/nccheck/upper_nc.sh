# usage: bash upper_nc.sh <tag> <abs sol> [extra]   (upperR2 with the no-clamp separator copy; Team A extended flags)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
TAG=$1; SOL=$2; shift 2; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; WK=$SC/P/wrnc_$TAG; mkdir -p $WK; D=$SC/eng_nc; cd $D
nice -n 12 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK "$@" > $D/upper_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [nc-$TAG] $SOL: $(grep 'UPPER-R2' $D/upper_$TAG.log | tail -1)" >> $D/nc.log
rm -rf $WK
