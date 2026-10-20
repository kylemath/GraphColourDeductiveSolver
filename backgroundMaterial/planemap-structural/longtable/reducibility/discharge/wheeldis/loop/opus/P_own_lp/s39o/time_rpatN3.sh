# s39o: separator timing, rpatN vs rpatN2 (vs rpatN3 with RS=), one exhaustive upperR2 pass (l3q-only flags) on sol_q39n
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; Q=$S/reg_A67; H=$B/s39o; cd $H/eng
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
A="root=$M args=$Q/args_A67.txt rpat=$B/rpatD.txt"; export OMP_NUM_THREADS=1
for R in ${RS:-rpatN rpatN2}; do t0=$(date +%s)
  nice -n 10 python3 pcheck.py upperR2 $FQ rpatN=$H/$R.txt nomax sol=$H/run_n/sol_q39n.json $A threads=1 work=$SC/P/wr39_time > $H/time_$R.log 2>&1
  echo "$R wall $(( $(date +%s)-t0 ))s" >> $H/time_$R.log; done
rm -rf $SC/P/wr39_time
