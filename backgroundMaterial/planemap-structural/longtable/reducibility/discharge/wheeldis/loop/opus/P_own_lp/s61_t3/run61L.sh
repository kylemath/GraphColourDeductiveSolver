# s61_t3 converged oracle: solveR2 fy fy2 toracle7, warm = standard set + all previous oracle rows (z-bearing). Resumable: each pass re-warms from every rows_q61L*.txt.
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s61_t3/env61.sh
RD=$Z61/run_L; mkdir -p $RD $RD/ckpt
WA83=$(ls $B/s44/eng/rows_q44fbA83*.txt $B/s44/run_A83/rows_q44fbA83*.txt 2>/dev/null | paste -sd, -)
W51=$(ls $B/s51/run_A87/rows_q51A87*.txt $B/s51/eng/rows_q51A87.txt 2>/dev/null | paste -sd, -); W47=$(ls $B/s47/run_A84/rows_q47A84*.txt 2>/dev/null | paste -sd, -)
BASEWARM=$Z/eng/rows_q60A97.txt,$B/s53/run_A97/rows_q53A97.txt,$WA83,$W47,$W51
note() { echo "$(date -u +%H:%M:%SZ) [s61L] $*" >> $Z61/run.log; }
cd $E
[ -e $RD/ckpt/seed_K_oracle.txt ] || cp rows_q61K_oracle.txt $RD/ckpt/seed_K_oracle.txt
for p in $(seq 1 ${NPASS:-6}); do
  [ -e $RD/converged ] && break
  WARM=$BASEWARM,$(ls $RD/ckpt/*.txt | paste -sd, -)
  note "pass $p start"
  nice -n 10 python3 pcheck.py solveR2 $FUP fy fy2 toracle7 $X f2b=$RULES keeppen tag=q61L_p$p $A $CB warm=$WARM K=300 xcap=3 xpen=1e-3 lpmax=45 maxit=400 threads=${THR:-3} work=$SC/s61/wL_p$p > $RD/L_p$p.log 2>&1
  rc=$?; cp rows_q61L_p$p.txt $RD/ckpt/rows_p$p.txt 2>/dev/null
  note "pass $p exit $rc: $(grep '^iter' $RD/L_p$p.log | tail -1 | cut -c1-120)"
  grep -q 'keeppen: stopping' $RD/L_p$p.log && { date -u > $RD/converged; cp sol_q61L_p$p.json $RD/sol_converged.json; }
done
note "L done"
