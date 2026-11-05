# s75 Team A K solve: s70 in-out K (rr z zr q7 flags as s69/s70) + s75 engine (moving in-point, probe, q7pen, per-iteration LP/in-point checkpoints).
# usage: bash runK75.sh <maxit> <threads> <tag> [extra pcheck args, e.g. inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 q7pen=1e-3]
# checkpoints (eng/): rows_<tag>.txt (rows added in THIS run, flushed per iteration), sol_<tag>_lp.json (LP point, per iteration), sol_<tag>_in.json (current in-point = upperR2 candidate)
# RESUME: cp eng/rows_<tag>.txt warm/rows_<tag>.txt ; cp eng/sol_<tag>_in.json warm/feas_<tag>.json (if it exists) ; WARM0=<previous WARM0>,$N/warm/rows_<tag>.txt, FEAS=$N/warm/feas_<tag>.json bash runK75.sh 200 2 <newtag> ... feasall
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s75_teamA/env75.sh
MI=$1; TH=$2; TAG=$3; shift 3; F="$FUP f2b=$RULES hat5 hatrr zh zr zcap=3 ${Q7F-q7 q7m q7rc q7cap=3}"; E=$N/eng; WK=$SC/P/wr75_$TAG; mkdir -p $N/runK_$TAG $WK; cp $SC/P/wr70/clsR2_1zfh.bin $WK/ 2>/dev/null
O=$B/s70_inout
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
W53=$B/s53/run_A97/rows_q53A97.txt
WARM0=${WARM0:-$O/warm/rows_q69rrz_snap2.txt,$O/warm/rows_q70t.txt,$O/warm/rows_q70inoutB.txt,}
FEAS=${FEAS:-$N/sol_feas.json}
WARM=${WARM0}$O/warm0_rows.txt,$B/s60_f2b/eng/rows_q60K95.txt,$B/s60_f2b/eng/rows_q60A97.txt,/mnt/project-files/swarm/teamA/R4-A1-motifs/cutP1_d7.txt,$W53,$WA83,$W47,$W51
cd $E
echo "$(date -u +%H:%M:%SZ) [s75K-$TAG] start: maxit $MI threads $TH feas $FEAS extra: $*  WARM0=$WARM0" >> $N/run.log
nice -n 15 python3 pcheck.py solveR2 $F $X keeppen tag=$TAG $A $CB warm=$WARM feas=$FEAS xcap=3 xpen=1e-3 lpmax=45 threads=$TH maxit=$MI work=$WK "$@" > $N/runK_$TAG/K.log 2>&1
cp sol_$TAG.json rows_$TAG.txt sol_${TAG}_in.json $N/runK_$TAG/ 2>/dev/null
echo "$(date -u +%H:%M:%SZ) [s75K-$TAG] ended: $(grep '^iter' $N/runK_$TAG/K.log | tail -1 | cut -c1-120)" >> $N/run.log
