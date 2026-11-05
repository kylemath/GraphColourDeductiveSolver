# Team C: trust-region LP at the in-point (trC.py) over a warm set. usage: [Q7F=""] bash runTR.sh <tag> <warm> <sol> <deltas> [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
C=$B/sC_tight; TAG=$1; WARM=$2; SOL=$3; DL=$4; shift 4; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 ${Q7F-q7 q7m q7rc q7cap=3}"; RD=$C/TR_$TAG; WK=$SC/sC/wT_$TAG; mkdir -p $RD $WK; cd $C
echo "$(date -u +%H:%M:%SZ) [sC-TR-$TAG] start warm=$WARM sol=$SOL deltas=$DL Q7F=${Q7F-q7 on} $*" >> $C/run.log
nice -n 15 python3 trC.py $F $X tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=1 work=$WK sol=$SOL outdir=$RD deltas=$DL "$@" > $RD/TR.log 2>&1
echo "$(date -u +%H:%M:%SZ) [sC-TR-$TAG] done: $(grep '^delta' $RD/TR.log | cut -c1-80 | paste -sd'|')" >> $C/run.log; echo DONE > $RD/DONE
rm -rf $WK
