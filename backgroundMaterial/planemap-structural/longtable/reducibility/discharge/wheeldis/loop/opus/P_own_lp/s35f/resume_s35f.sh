# s35f resume script (restart-safe). fy, s24d flags, no l3q, argsA63 (413ba030), threads=2, cap 5 h per solve run.
# keeppen runs are tagged s35f, s35f2, s35f3, ...; each warm-starts from every rows_s35f*.txt already on disk (+ base warm).
# A keeppen run that finishes (converged or capped) writes keep_done.txt = its tag. Then nosep (s35fL), lowerR2, upperR2.
# Re-run this script after any restart: it skips finished stages and continues from the newest rows.
P=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp
Q=$P/s35f; cd $Q
S=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad
M=$S/P/m/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
A="root=$M args=$Q/argsA63.txt rpat=$P/rpatD.txt"
F="xon apexcls filt16 killtab=$Q/f/kill/kill6 hat5 consall fy"
CB=consbasis=$P/s21/cf/cons2basis_cls.json
BASE=$P/s25c/rows_st25y.txt,$P/s28q/eng/rows_s28A62.txt
TH=2
allrows(){ ls -t rows_s35f*.txt 2>/dev/null | grep -v 'rows_s35fL' | tr '\n' ',' | sed 's/,$//'; }
if [ ! -f keep_done.txt ]; then
  n=1; while [ -f s35f$( [ $n -gt 1 ] && echo $n )_start.txt ]; do n=$((n+1)); done
  tag=s35f$( [ $n -gt 1 ] && echo $n ); W=$(allrows); W=${W:+$W,}$BASE
  echo "$(date -u +%H:%M:%SZ) keeppen $tag warm=$W" >> resume.log
  date -u +%H:%M:%SZ > ${tag}_start.txt
  timeout 18000 nice -n 5 python3 pcheck.py solveR2 $F keeppen tag=$tag $A $CB warm=$W K=300 xcap=3 xpen=1e-3 threads=$TH work=$S/P/wr35_$tag > $tag.log 2>&1; rc=$?
  echo "solve exit $rc" >> $tag.log; date -u +%H:%M:%SZ > ${tag}_end.txt
  echo $tag > keep_done.txt
fi
KT=$(cat keep_done.txt)
if [ ! -f done_L.txt ]; then
  W=$(allrows); echo "$(date -u +%H:%M:%SZ) nosep warm=$W,$BASE" >> resume.log
  timeout 18000 nice -n 5 python3 pcheck.py solveR2 $F nosep tag=s35fL $A $CB warm=$W,$BASE K=300 xcap=3 threads=$TH work=$S/P/wr35_s35fL > s35fL.log 2>&1 && date -u +%H:%M:%SZ > done_L.txt
fi
[ -f lower_s35fL.log ] && grep -q LOWER-R2 lower_s35fL.log || nice -n 5 python3 pcheck.py lowerR2 $F cert=cert_s35fL.json xcap=3 $A work=$S/P/wr35_s35fL > lower_s35fL.log 2>&1
for sol in sol_$KT.json sol_s35fL.json; do
  [ -f $sol ] || continue; u=upper_${sol#sol_}; u=${u%.json}.log
  [ -f $u ] && grep -q UPPER-R2 $u || nice -n 5 python3 pcheck.py upperR2 $F nomax sol=$sol $A threads=$TH work=$S/P/wr35_u > $u 2>&1
done
md5sum sol_*.json cert_*.json rows_s35f*.txt > md5_out.txt 2>&1
echo DONE > done.txt
