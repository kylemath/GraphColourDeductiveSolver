# Team C: nosep L (no x penalty) over a given warm row set + lowerR2 on its cert (runL75.sh flags; engine copy sC_tight/eng).
# usage: [Q7F=""] bash runLC.sh <tag> <warm csv> [extra solveR2 args]
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
C=$B/sC_tight; TAG=$1; WARM=$2; shift 2; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 ${Q7F-q7 q7m q7rc q7cap=3}"; RD=$C/L_$TAG; WK=$SC/sC/wL_$TAG; mkdir -p $RD $WK; cd $C/eng
echo "$(date -u +%H:%M:%SZ) [sC-L-$TAG] start warm=$WARM Q7F=${Q7F-q7 on} extra: $*" >> $C/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X nosep tag=$TAG $A $CB warm=$WARM K=300 xcap=3 threads=1 work=$WK "$@" > $RD/L.log 2>&1
mv sol_$TAG.json cert_$TAG.json $RD/; rm -f rows_$TAG.txt sol_${TAG}_lp.json
nice -n 15 python3 pcheck.py lowerR2 $F $X cert=$RD/cert_$TAG.json xcap=3 $A work=$WK > $RD/lower.log 2>&1
echo "$(date -u +%H:%M:%SZ) [sC-L-$TAG] $(grep '^nosep' $RD/L.log | cut -c1-90) ; $(grep LOWER-R2 $RD/lower.log | tail -1 | cut -c1-120)" >> $C/run.log; echo DONE > $RD/DONE
[ -z "$KEEPWK" ] && rm -rf $WK
