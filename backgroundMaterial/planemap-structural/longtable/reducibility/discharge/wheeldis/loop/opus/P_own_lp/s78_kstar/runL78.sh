# s78: L (nosep, NO x penalty) over a warm row set (+ lowerR2 on its cert unless NOLOWER=1), s78 engine.  usage: [STACK=..] [FAM=..] [KS=0|1] bash runL78.sh <tag> <warm csv> [threads] [extra]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s78_kstar/env78.sh
TAG=$1; WARM=$2; TH=${3:-1}; shift 3; RD=$N/runL_$TAG; WK=$SD/wr78L_$TAG; mkdir -p $RD $WK; cd $N/eng
echo "$WARM" > $RD/warmlist.txt
echo "$(date -u +%H:%M:%SZ) [s78L-$TAG] start STACK=${STACK:-s75} FAM=${FAM:-full} KS=${KS:-0} threads $TH warm $(echo $WARM | tr , '\n' | wc -l) files extra: $*" >> $N/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=$WK "$@" > $RD/L.log 2>&1
cp sol_$TAG.json cert_$TAG.json $RD/ && rm -f sol_$TAG.json cert_$TAG.json rows_$TAG.txt
[ -z "$NOLOWER" ] && nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$RD/cert_$TAG.json xcap=3 $A work=$WK > $RD/lower.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s78L-$TAG] $(grep '^nosep' $RD/L.log | cut -c1-90) ; $(grep LOWER-R2 $RD/lower.log 2>/dev/null | tail -1 | cut -c1-120)" >> $N/run.log; echo DONE > $RD/DONE
[ -z "$KEEPWK" ] && rm -rf $WK
