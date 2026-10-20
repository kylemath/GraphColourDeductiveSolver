# s35f round 3 on registry A67 (argsA67, main 2c97e14d out/job30; k3x and kill npy byte-identical to A63/413ba030, see ../a67_same_as_A63.txt).
# fy, s24d flags, no l3q; nice -n 15 (lowest priority), threads=2, cap 5 h per solve. Warm: every ../rows_s35f*.txt + rows here + base.
# Restart-safe like ../resume_s35f.sh. Kill tables: s33z/reg_A67/f/kill (A67's own with-C tables).
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Q=$P/s35f/a67; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
A="root=$M args=$P/s33z/argsA67.txt rpat=$P/rpatD.txt"
F="xon apexcls filt16 killtab=$P/s33z/reg_A67/f/kill/kill6 hat5 consall fy"
CB=consbasis=$P/s21/cf/cons2basis_cls.json
BASE=$P/s25c/rows_st25y.txt,$P/s28q/eng/rows_s28A62.txt
TH=2; NI="nice -n 15"; cp ../pcheck.py ../prelay.py ../prelay2.py ../pslite.py ../psolve.py . 2>/dev/null; [ -d bin ] || cp -r ../bin .
allrows(){ ls -t ../rows_s35f*.txt rows_a67*.txt 2>/dev/null | grep -v 'L.txt' | tr '\n' ',' | sed 's/,$//'; }
if [ ! -f keep_done.txt ]; then
  n=1; while [ -f a67k${n}_start.txt ]; do n=$((n+1)); done; tag=a67k$n; W=$(allrows); W=${W:+$W,}$BASE
  echo "$(date -u +%H:%M:%SZ) keeppen $tag warm=$W" >> resume.log; date -u +%H:%M:%SZ > ${tag}_start.txt
  timeout 18000 $NI python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$W K=300 xcap=3 xpen=1e-3 threads=$TH work=$S/P/wr35a_$tag > $tag.log 2>&1; echo "solve exit $?" >> $tag.log
  date -u +%H:%M:%SZ > ${tag}_end.txt; echo $tag > keep_done.txt
fi
KT=$(cat keep_done.txt)
if [ ! -f done_L.txt ]; then W=$(allrows); echo "$(date -u +%H:%M:%SZ) nosep" >> resume.log
  timeout 18000 $NI python3 pcheck.py solveR2 $F nosep tag=a67L $A $CB warm=$W,$BASE K=300 xcap=3 threads=$TH work=$S/P/wr35a_L > a67L.log 2>&1 && date -u +%H:%M:%SZ > done_L.txt; fi
grep -q LOWER-R2 lower_a67L.log 2>/dev/null || $NI python3 pcheck.py lowerR2 $F cert=cert_a67L.json xcap=3 $A work=$S/P/wr35a_L > lower_a67L.log 2>&1
[ -f sol_$KT.json ] && { grep -q UPPER-R2 upper_$KT.log 2>/dev/null || $NI python3 pcheck.py upperR2 $F nomax sol=sol_$KT.json $A threads=$TH work=$S/P/wr35a_u > upper_$KT.log 2>&1; }
md5sum sol_*.json cert_*.json rows_a67*.txt > md5_out.txt 2>&1; echo DONE > done.txt
