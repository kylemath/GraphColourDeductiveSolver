# short K solve (pricing pointer).  usage: bash runK67.sh <tag> <maxit> [flags...]   (threads=3, nice 15; engine s67/eng; warm = s64 rows snapshot + the run64 warm set)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s67_q7/env67.sh
TAG=$1; MI=$2; shift 2; F="$FUP f2b=$RULES"; E=$N/eng; WK=$SC/P/wr67$TAG; mkdir -p $N/runK_$TAG
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt
WARM=$N/warm0_rows.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$W53,$WA83,$W47,$W51
cd $E
nice -n 10 python3 pcheck.py solveR2 $F $X keeppen tag=q67$TAG $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=45 threads=3 maxit=$MI work=$WK "$@" > $N/runK_$TAG/K.log 2>&1
cp sol_q67$TAG.json rows_q67$TAG.txt $N/runK_$TAG/ 2>/dev/null
