# s39o control (a): flag off (no offc, no rpatN) on the s39o engine reproduces the A67 q66 numbers (s33z/run_A67).
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
S=$B/s33z; RD=$S/run_A67; Q=$S/reg_A67; H=$B/s39o; cd $H/eng
SC=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad; M=$SC/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
A="root=$M args=$Q/args_A67.txt rpat=$B/rpatD.txt"
export OMP_NUM_THREADS=1
nice -n 10 python3 pcheck.py lowerR2 $FQ cert=$RD/cert_q66L.json xcap=3 $A work=$SC/P/wr39_ctlA > $H/ctlA_lower.log 2>&1
nice -n 10 python3 pcheck.py upperR2 $FQ nomax sol=$RD/sol_q66.json $A threads=1 work=$SC/P/wr39_ctlA > $H/ctlA_upper.log 2>&1
nice -n 10 python3 pcheck.py binderR2 $FQ $A sol=$RD/sol_q66L.json cert=$RD/cert_q66L.json row=7:8666655:5677657 top=15 work=$SC/P/wr39_ctlA > $H/ctlA_binders.log 2>&1
strip() { sed -E 's/[0-9.]+s\)/Xs)/g; s/\([0-9.]+s/(Xs/g; s/ [0-9.]+s / Xs /g' "$1"; }
for p in "lower lower_q66L" "upper upper_q66" "binders binders_q66L"; do set -- $p
  if diff <(strip $H/ctlA_$1.log) <(strip $RD/$2.log) > $H/ctlA_$1.diff; then echo "$1: IDENTICAL to run_A67/$2.log (timings masked)"; else echo "$1: DIFFERS ($(wc -l < $H/ctlA_$1.diff) diff lines)"; fi
done > $H/ctlA_result.txt
grep -h "LOWER-R2\|UPPER-R2" $H/ctlA_lower.log $H/ctlA_upper.log >> $H/ctlA_result.txt
