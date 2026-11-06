# s85 world LP: the 5/6/7 world (receivers = <rows> file, every sender row, every cons2 class row) with generic keys, no separation.
# usage: STACK=s77 ARGS=<args> bash world85.sh <tag> <rows> <gkeys file> "<extra flags>"   (FAM=full, KS=0: K* enters as the generic key KS)
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; Z=$B/s85_edge56
export FAM=full KS=0; . $Z/env85.sh
TG=$1; ROWS=$2; KEYS=$3; XF=$4; RD=$Z/run_$TG; WK=$SD/wr85_$TG; mkdir -p $RD $WK; cd $E85
echo "$(date -u +%H:%M:%SZ) [s85W-$TG] start STACK=$STACK ARGS=$(basename $ARGS) FAM=$FAM rows $(basename $ROWS) ($(wc -l < $ROWS)) gkeys $(basename $KEYS) (md5 $(md5sum $KEYS | cut -c1-8)) flags: $XF" >> $Z/run.log
nice -n 12 python3 pcheck.py solveR2 $F $X nosep tag=$TG $A consbasis=$Z/world/cons2_all_57.json warm=$ROWS K=300 xcap=3 threads=1 lpmax=45 work=$WK gkeys=$KEYS $XF > $RD/L.log 2>&1
mv sol_$TG.json cert_$TG.json rows_$TG.txt sol_${TG}_lp.json $RD/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s85W-$TG] $(grep '^nosep' $RD/L.log | cut -c1-90) | $(grep 'R6x2' $RD/L.log | cut -c1-120) | $(grep -c Traceback $RD/L.log) tracebacks" >> $Z/run.log
rm -rf $WK; echo DONE > $RD/DONE
