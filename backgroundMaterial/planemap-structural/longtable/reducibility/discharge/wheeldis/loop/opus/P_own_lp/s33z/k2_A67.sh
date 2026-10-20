# K2 on A67: the xpen=1e-3 keeppen (K run 2, t = 0.125836 FEASIBLE) leaves a wide gap to the nosep lower (0.103862): the penalty
# (1e-3 per unit on x/D/lq/z/zr/rr/z6, all capped at 3) is what the keeppen t pays. Re-run keeppen warm with xpen=1e-5 (same caps,
# lpmax=1500) from every rows file incl. K run 2's (rows_s33_rK1p3.txt); then resume_s33.sh redoes L (nosep, lowerR2, upperR2), N, U, X, C, B.
# xpen=1e-3 results kept in run_A67/p3/.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; RD=$S/run_A67; Q=$S/reg_A67; cd $S/eng
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
export OMP_NUM_THREADS=1
A="root=$M args=$Q/args_A67.txt rpat=$B/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3 zh zr hatrr zcap=3 l6r z6cap=3 pcell=$S/pcell/k3p.txt"
CB=consbasis=$B/s21/cf/cons2basis_cls.json
true
WARM=$(cat $RD/warm_K.txt)
echo "$(date -u +%H:%M:%SZ) [A67] K2 (xpen=1e-5) start" >> $S/wait.log
date -u +%H:%M:%SZ > $RD/K2_start.txt
timeout 10800 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=s33 $A $CB warm=$WARM K=300 xcap=3 xpen=1e-5 lpmax=60 threads=2 work=$SC/P/wr_A67s2 > $RD/s33_K2.log 2>&1; ec=$?
if [ $ec = 0 ] && [ sol_s33.json -nt $RD/K2_start.txt ]; then
  cp sol_s33.json rows_s33.txt $RD/; cp rows_s33.txt rows_s33_rK2.txt; rm -f $RD/L.done $RD/N.done; date -u +%H:%M:%SZ > $RD/K2.done
  echo "$(date -u +%H:%M:%SZ) [A67] K2 converged: $(grep '^iter' $RD/s33_K2.log | tail -1 | cut -c1-40)" >> $S/wait.log
  cd $S && bash resume_s33.sh A67 2c97e14d > $S/resume_A67.out 2>&1
else echo "$(date -u +%H:%M:%SZ) [A67] K2 exit $ec (not converged)" >> $S/wait.log; fi
