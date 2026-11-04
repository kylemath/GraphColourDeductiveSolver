# s70 in-out separated K solve (rr z zr q7 flags as s69) + inout separation.  usage: bash runK70.sh <maxit> <threads> <tag> [extra pcheck args e.g. inout=0.3,0.8,0.1 inoutk=4]
# nice 15.  engine s70_inout/eng (pcheck.py + pinout.py + prelay2.py sepround).  checkpoint: eng/rows_<tag>.txt (rows added in THIS run, rewritten each iteration -- put it first in WARM0 on resume).
# RESUME: cp eng/rows_<tag>.txt warm/rows_<tag>_resume.txt ; WARM0=$PWD/warm/rows_<tag>_resume.txt, ; export WARM0 ; bash runK70.sh 200 2 <newtag> inout=...   (warm admission takes ~35-60 min)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s70_inout/env70.sh
MI=$1; TH=$2; TAG=$3; shift 3; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 q7 q7m q7rc q7cap=3"; E=$N/eng; WK=$SC/P/wr70_$TAG; mkdir -p $N/runK_$TAG $WK; cp $SC/P/wr70/clsR2_1zfh.bin $WK/ 2>/dev/null
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt
WARM0=${WARM0:-$N/warm/rows_q69rrz_snap.txt,}
WARM=${WARM0}$N/warm0_rows.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$W53,$WA83,$W47,$W51
cd $E
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$N/sol_feas.json K=300 xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK "$@" > $N/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt $N/runK_$TAG/ 2>/dev/null
