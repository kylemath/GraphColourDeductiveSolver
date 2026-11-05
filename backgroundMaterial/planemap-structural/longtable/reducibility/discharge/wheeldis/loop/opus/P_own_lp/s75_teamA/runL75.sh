# s75 Team A: L (nosep, no x penalty) over a given warm row set + lowerR2 on its cert, extended stack (rr z zr q7).  usage: bash runL75.sh <tag> <warm csv> [threads]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
TAG=$1; WARM=$2; TH=${3:-1}; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 ${Q7F-q7 q7m q7rc q7cap=3}"; RD=$N/runL_$TAG; WK=$SC/P/wr75L_$TAG; mkdir -p $RD $WK; cd $N/eng
nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=$TH work=$WK > $RD/L.log 2>&1
cp sol_$TAG.json cert_$TAG.json $RD/
nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$RD/cert_$TAG.json xcap=3 $A work=$WK > $RD/lower.log 2>&1
echo "$(date -u +%H:%M:%SZ) [s75L-$TAG] $(grep '^nosep' $RD/L.log | cut -c1-90) ; $(grep LOWER-R2 $RD/lower.log | tail -1 | cut -c1-120)" >> $N/run.log; echo DONE > $RD/DONE
[ -z "$KEEPWK" ] && rm -rf $WK
