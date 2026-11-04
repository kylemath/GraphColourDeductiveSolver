# L (nosep) + lowerR2 from the current K rows (partial or converged).  usage: bash runL64.sh [suffix]
. $(dirname $(readlink -f $0))/env64.sh
SFX=${1:-x}; RD=$N/runL_$SFX; mkdir -p $RD; WK=$SC/P/wr64L$SFX; TL=q64F$SFX; NI=10
F="$FUP f2b=$RULES"; E=$N/eng; cd $E
note() { echo "$(date -u +%H:%M:%SZ) [s64L-$SFX] $*" >> $N/run.log; }
cp rows_q64F.txt $RD/rows_snapshot.txt
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
WARM=$RD/rows_snapshot.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$B/s53/run_A97/rows_q53A97.txt,$WA83,$W47,$W51
nice -n $NI python3 pcheck.py solveR2 $F $X nosep tag=$TL $A $CB warm=$WARM K=300 xcap=3 threads=1 work=${WK}L > $RD/L.log 2>&1
cp sol_$TL.json cert_$TL.json $RD/ 2>&1
note "L nosep: $(grep '^nosep' $RD/L.log | cut -c1-90)"
nice -n $NI python3 pcheck.py lowerR2 $F $X cert=$RD/cert_$TL.json xcap=3 $A work=${WK}L > $RD/lower.log 2>&1
note "lower: $(grep LOWER-R2 $RD/lower.log | tail -1 | cut -c1-100)"; echo DONE > $RD/DONE
