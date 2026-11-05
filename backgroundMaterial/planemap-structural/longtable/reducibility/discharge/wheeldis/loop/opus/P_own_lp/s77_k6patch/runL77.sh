# s77: L (nosep, NO x penalty; LEXTRA="lpmax=45" = simplex 45 s then IPM + simplex polish, as in the K) over a warm row set + lowerR2 on its cert, patched stack, families FAM (base|rrz|full).  usage: [FAM=..] [KT=..] bash runL77.sh <tag> <warm csv> [threads]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s77_k6patch/env77.sh
TAG=$1; WARM=$2; TH=${3:-1}; RD=$N/runL_$TAG; WK=$S7/wr77L_$TAG; mkdir -p $RD $WK; cd $N/eng
echo "$WARM" > $RD/warmlist.txt
echo "$(date -u +%H:%M:%SZ) [s77L-$TAG] start FAM=${FAM:-base} KT=$KT threads $TH warm $(echo $WARM | tr , '\n' | wc -l) files" >> $N/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=$WK $LEXTRA > $RD/L.log 2>&1
cp sol_$TAG.json cert_$TAG.json $RD/
nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$RD/cert_$TAG.json xcap=3 $A work=$WK > $RD/lower.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s77L-$TAG] FAM=${FAM:-base} $(grep '^nosep' $RD/L.log | cut -c1-90) ; $(grep LOWER-R2 $RD/lower.log | tail -1 | cut -c1-120) ; cert md5 $(md5sum < $RD/cert_$TAG.json | cut -c1-32)" >> $N/run.log; echo DONE > $RD/DONE
[ -z "$KEEPWK" ] && rm -rf $WK
