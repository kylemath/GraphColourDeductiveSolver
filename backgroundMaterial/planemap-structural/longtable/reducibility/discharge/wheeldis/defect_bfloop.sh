#!/bin/bash
# usage: defect_bfloop.sh CANDS WORKPREFIX TAG  (README §7.3.1; exploratory). Checks candidates against R_opt+ (defect_check2.py bf),
# runs dfast (ring <= 16) on the configurations still needed, writes out/def_loop_<TAG>_<n>.out, and repeats until nothing is left.
W=/home/claude/gcds/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W
C=$1; WK=$2; T=$3
for n in 1 2 3 4 5 6; do
  python3 defect_check2.py $C $WK bf | tail -2
  awk '$2<=16' $WK.d > $WK.d$n.in
  [ -s $WK.d$n.in ] || break
  echo "round $n dfast $(wc -l < $WK.d$n.in)"
  bin/dfast $WK.d$n.in > out/def_loop_${T}_$n.out 2>&1
done
echo "bfloop done"; grep -v '^killed' $WK.status | cut -c1-200
