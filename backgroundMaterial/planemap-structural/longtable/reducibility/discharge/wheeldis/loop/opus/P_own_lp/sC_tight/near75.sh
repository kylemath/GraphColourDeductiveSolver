# Team C: list near-tight receiver rows at an in-point (upperR2 with eps<0 = threshold lowered by |eps|; every row with slack < |eps| written to vfile)
# usage: bash near75.sh <tag> <ABS sol json> <eps e.g. -0.01> [extra pcheck args]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
C=$B/sC_tight; TAG=$1; SOL=$2; EP=$3; shift 3; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; WK=$SC/sC/wk_$TAG; mkdir -p $WK; cd $N/eng
rm -f $C/near_$TAG.txt
echo "$(date -u +%H:%M:%SZ) [sC-near-$TAG] start sol=$SOL eps=$EP" >> $C/run.log
nice -n 15 python3 pcheck.py upperR2 $F $X nomax sol=$SOL $A threads=1 work=$WK eps=$EP vK=400000 vfile=$C/near_$TAG.txt "$@" > $C/near_$TAG.log 2>&1
echo "$(date -u +%H:%M:%SZ) [sC-near-$TAG] done: $(grep 'UPPER-R2' $C/near_$TAG.log | tail -1) rows $(wc -l < $C/near_$TAG.txt)" >> $C/run.log
[ -z "$KEEPWK" ] && rm -rf $WK
