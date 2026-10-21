# s51 control (d): smoke solves with xo on A78 (s42a arguments; nice 10, threads 1)
#  s1: nosep LP over all s42a rows (rows_q42aA78.txt) with xo, then lowerR2 xo on its cert (compare with s42a L t)
#  s2: separation smoke: warm = the same rows, maxit=3 (2 separation rounds d = 7..17 with the xo window), then lowerR2 xo
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s51/env51.sh
CB=consbasis=$B/s21/cf/cons2basis_cls.json; WR=$B/s42a/run_A78/rows_q42aA78.txt; cd $E
for s in s1 s2; do
  O=$D/ctl_d_$s; mkdir -p $O; note "smoke $s start"
  if [ $s = s1 ]; then EXTRA=nosep; else EXTRA="maxit=3 xpen=1e-3 keeppen"; fi
  nice -n 10 python3 pcheck.py solveR2 $FQ $X xo $EXTRA tag=s51$s $A $CB warm=$WR K=300 xcap=3 threads=1 work=$SC/P/wr51_$s > $O/solve.log 2>&1
  mv sol_s51$s.json cert_s51$s.json rows_s51$s.txt $O/
  nice -n 10 python3 pcheck.py lowerR2 $FQ $X xo cert=$O/cert_s51$s.json xcap=3 $A work=$SC/P/wr51_$s > $O/lower.log 2>&1
  python3 -c "
import json; S = json.load(open('$O/sol_s51$s.json')); C = json.load(open('$O/cert_s51$s.json'))
xo = S['xo']; print('sol t %.12f: xoflag %s, old x %d, xo > 0: %d (sum %.6f, max %.6f); cert mrowX rows %d of %d' % (S['t'], S['xoflag'], len(S['x']), len(xo), sum(xo.values()), max(xo.values() or [0]), sum(1 for c in C if c['row'][0] == 'mrowX'), len(C)))" > $O/summary.txt
  note "smoke $s: $(grep -E '^(nosep|iter)' $O/solve.log | tail -1 | cut -c1-90) | $(grep LOWER-R2 $O/lower.log | tail -1) | $(cat $O/summary.txt)"
done
echo DONE > $D/ctl51d.done
