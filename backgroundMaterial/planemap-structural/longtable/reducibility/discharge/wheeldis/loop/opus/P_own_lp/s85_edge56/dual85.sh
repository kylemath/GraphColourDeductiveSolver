# s85: dual of a K run's LP without stopping it: nosep solve over the run's warm list + a snapshot of its separated rows (same stack and keys,
# no penalties) -> eng cert_<tag>.json (row duals).  usage: [STACK ARGS KEYS] bash dual85.sh <tag> <warm csv> "<flags>"
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56
export FAM=full KS=0; unset EGK; . $Z/env85.sh
TG=$1; WARMC=$2; XF=$3; RD=$Z/run_$TG; WK=$SD/wr85_$TG; mkdir -p $RD $WK; cd $E85
echo "$(date -u +%H:%M:%SZ) [s85D-$TG] start STACK=$STACK ARGS=$(basename $ARGS) gkeys $(basename $KEYS) flags: $XF" >> $Z/run.log
nice -n 12 python3 pcheck.py solveR2 $F $X nosep tag=$TG $A $CB warm=$WARMC K=300 xcap=3 threads=1 lpmax=45 work=$WK gkeys=$KEYS $XF > $RD/L.log 2>&1
mv sol_$TG.json cert_$TG.json rows_$TG.txt sol_${TG}_lp.json $RD/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s85D-$TG] $(grep '^nosep\|^LP t\*' $RD/L.log | head -2 | cut -c1-120 | tr '\n' ' ') $(grep -c Traceback $RD/L.log) tracebacks" >> $Z/run.log
rm -rf $WK; echo DONE > $RD/DONE
