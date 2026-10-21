# s51 control (d) s3: nosep LP (xo) over the s42a rows + the rows smoke s2 separated with the xo window, then lowerR2 xo (the L-stage path)
. /home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s51/env51.sh
CB=consbasis=$B/s21/cf/cons2basis_cls.json; O=$D/ctl_d_s3; mkdir -p $O; cd $E; note "smoke s3 start"
nice -n 10 python3 pcheck.py solveR2 $FQ $X xo nosep tag=s51s3 $A $CB warm=$D/ctl_d_s2/rows_s51s2.txt,$B/s42a/run_A78/rows_q42aA78.txt K=300 xcap=3 threads=1 work=$SC/P/wr51_s3 > $O/solve.log 2>&1
mv sol_s51s3.json cert_s51s3.json rows_s51s3.txt $O/
nice -n 10 python3 pcheck.py lowerR2 $FQ $X xo cert=$O/cert_s51s3.json xcap=3 $A work=$SC/P/wr51_s3 > $O/lower.log 2>&1
python3 -c "
import json; S = json.load(open('$O/sol_s51s3.json')); C = json.load(open('$O/cert_s51s3.json'))
xo = S['xo']; print('sol t %.12f: xo > 0: %d (sum %.6f, max %.6f); cert mrowX rows %d of %d' % (S['t'], len(xo), sum(xo.values()), max(xo.values() or [0]), sum(1 for c in C if c['row'][0] == 'mrowX'), len(C)))" > $O/summary.txt
note "smoke s3 (nosep over s42a + s2 rows): $(grep -E '^nosep' $O/solve.log | cut -c1-80) | $(grep LOWER-R2 $O/lower.log | tail -1 | cut -c1-120) | $(cat $O/summary.txt)"
echo DONE > $D/ctl51d3.done
