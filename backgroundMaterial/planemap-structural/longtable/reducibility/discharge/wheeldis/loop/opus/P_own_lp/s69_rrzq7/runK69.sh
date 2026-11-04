# s69 separated K solve, flags hat5 hatrr zh zr zcap=3 + q7 q7m q7rc q7cap=3.  usage: bash runK69.sh <maxit>   (threads=2, nice 15; engine s69/eng)
# RESUME: rows_q69rrz.txt (eng/, rewritten each iteration) is the checkpoint; to resume add it first in WARM below (WARM=eng/rows_q69rrz.txt,...) and rerun with a new tag/ copy.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s69_rrzq7/env69.sh
MI=$1; shift 1; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; E=$N/eng; WK=$SC/P/wr69; mkdir -p $N/runK $WK
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt
WARM=${WARM0}$N/warm0_rows.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$W53,$WA83,$W47,$W51
cd $E
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=q69rrz $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=45 threads=2 maxit=$MI work=$WK "$@" > $N/runK/K.log 2>&1
cp sol_q69rrz.json rows_q69rrz.txt $N/runK/ 2>/dev/null
