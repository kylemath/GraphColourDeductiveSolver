# s35f-fyq: l3q + fy re-solve on A67 (gate passed: pricer35 most negative fy rc on cert_q66L = -31300/438047 = -0.0715).
# Engine fyq/eng = s33z/eng + port_fy.py (fy hooks from s25c). Flags = q66's FQ + fy. nice 15, threads=2, 5 h cap per solve.
# Restart-safe: each stage leaves a marker in fyq/.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
D=$P/s35f/fyq; E=$D/eng; Q=$P/s33z/reg_A67; cd $E
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
A="root=$M args=$Q/args_A67.txt rpat=$P/rpatD.txt"
FQ="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall l3q l3qtab=$Q/tab_1.json,$Q/tab_-1.json lqcap=3"
F="$FQ fy"; CB=consbasis=$P/s21/cf/cons2basis_cls.json; TH=2; export OMP_NUM_THREADS=1
Z=$P/s33z/eng
WB=$Z/rows_q66.txt,$Z/rows_q66A66a.txt,$Z/rows_s33A66a.txt,$Z/rows_s33A64.txt,$Z/rows_q64A64.txt,$P/s35f/rows_s35f2.txt,$P/s35f/rows_s35f.txt,$P/s25c/rows_st25y.txt,$P/s28q/eng/rows_s28A62.txt,$P/s28q/eng/rows_s28A60.txt
note() { echo "$(date -u +%H:%M:%SZ) $*" >> $D/run.log; }
# controls: the ported engine without fy reproduces cert_q66L; with fy the old cert must fail (z columns rc < 0)
[ -e $D/ctl_lower_nofy.log ] || nice -n 15 python3 pcheck.py lowerR2 $FQ cert=$P/s33z/run_A67/cert_q66L.json xcap=3 $A work=$S/P/wr35_fyq > $D/ctl_lower_nofy.log 2>&1
[ -e $D/ctl_lower_fy.log ] || nice -n 15 python3 pcheck.py lowerR2 $F cert=$P/s33z/run_A67/cert_q66L.json xcap=3 $A work=$S/P/wr35_fyq > $D/ctl_lower_fy.log 2>&1
[ -e $D/ctl_upper_fy_q66.log ] || nice -n 15 python3 pcheck.py upperR2 $F nomax sol=$P/s33z/run_A67/sol_q66.json $A threads=$TH work=$S/P/wr35_fyqu > $D/ctl_upper_fy_q66.log 2>&1
note "controls: $(grep -h 'LOWER-R2\|UPPER-R2' $D/ctl_*.log | tr '\n' ' ')"
if [ ! -e $D/K.done ]; then
  n=1; while [ -e $D/K${n}_start.txt ]; do n=$((n+1)); done; tag=fyq$n
  WS=$(ls -t rows_fyq[0-9]*.txt 2>/dev/null | paste -sd, -); W=${WS:+$WS,}$WB
  note "keeppen $tag warm=$W"; date -u +%H:%M:%SZ > $D/K${n}_start.txt
  timeout 18000 nice -n 15 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$W K=300 xcap=3 xpen=1e-3 threads=$TH work=$S/P/wr35_$tag > $D/$tag.log 2>&1; ec=$?
  note "keeppen $tag exit $ec"; echo $tag > $D/K.done
fi
KT=$(cat $D/K.done)
if [ ! -e $D/L.done ]; then
  W=$(ls -t rows_fyq[0-9]*.txt | paste -sd, -),$WB; note "nosep fyqL"
  timeout 18000 nice -n 15 python3 pcheck.py solveR2 $F nosep tag=fyqL $A $CB warm=$W K=300 xcap=3 threads=$TH work=$S/P/wr35_fyqL > $D/fyqL.log 2>&1 && date -u +%H:%M:%SZ > $D/L.done
fi
grep -q LOWER-R2 $D/lower_fyqL.log 2>/dev/null || nice -n 15 python3 pcheck.py lowerR2 $F cert=cert_fyqL.json xcap=3 $A work=$S/P/wr35_fyqL > $D/lower_fyqL.log 2>&1
for t in $KT fyqL; do
  [ -e sol_$t.json ] || continue
  grep -q UPPER-R2 $D/upper_$t.log 2>/dev/null || nice -n 15 python3 pcheck.py upperR2 $F nomax sol=sol_$t.json $A threads=$TH work=$S/P/wr35_fyqu > $D/upper_$t.log 2>&1
done
cp sol_*.json cert_*.json rows_fyq*.txt $D/ 2>/dev/null; (cd $D && md5sum sol_*.json cert_*.json rows_fyq*.txt > md5_out.txt)
note "DONE: $(grep -h 'LOWER-R2\|UPPER-R2' $D/lower_fyqL.log $D/upper_*.log | tr '\n' ' ')"; echo DONE > $D/done.txt
