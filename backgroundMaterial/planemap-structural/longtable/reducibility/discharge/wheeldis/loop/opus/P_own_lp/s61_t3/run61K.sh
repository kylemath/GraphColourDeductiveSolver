# s61_t3 STEP 2: short K stages (maxit iterations) from the s60 warm set: oracle (fy fy2 toracle7), fy2 (empty tkill), fy off.
# usage: MAXIT=4 bash run61K.sh     (2 threads; each run: warm admission ~6-10 min + ~3-4 min per iteration)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s61_t3/env61.sh
RD=$Z61/run_K; mkdir -p $RD; NI=${MAXIT:-4}
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
WARM=$Z/eng/rows_q60A97.txt,$B/s53/run_A97/rows_q53A97.txt,$WA83,$W47,$W51
note() { echo "$(date -u +%H:%M:%SZ) [s61K] $*" >> $Z61/run.log; }
cd $E
for cfg in "oracle:fy fy2 toracle7" "fy2:fy fy2" "off:"; do
  n=${cfg%%:*}; fl=${cfg#*:}
  [ -e $RD/$n.done ] && continue
  note "K $n start (flags '$fl', maxit $NI)"
  timeout ${TO:-5400} nice -n 10 python3 pcheck.py solveR2 $FUP $fl $X f2b=$RULES keeppen tag=q61K_$n $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=45 maxit=$NI threads=2 work=$SC/s61/wK_$n > $RD/K_$n.log 2>&1
  note "K $n exit $?: $(grep '^iter' $RD/K_$n.log | tail -1 | cut -c1-90)"; date -u > $RD/$n.done
done
note "all K runs done"
