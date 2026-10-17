#!/bin/bash
# EXPLORE round 26: round 20/23's transfer LP with every explore window as a pattern, to convergence or 45 minutes.
# l2.py names its output l2_x_w_dump.txt in loop/l2 (committed from round 24), so it is moved to n9/l2_r26.txt and restored.
cd "$(dirname "$0")/../l2"
cp l2_x_w_dump.txt l2_x_w_dump.txt.keep
nice -n 5 python3 l2.py maxit=60 tmax=2700 pat=loop/w2/win14.out pat=loop/w2/win8.out pat=loop/w2/win89.out \
  pat=loop/n9/win9.out pat=loop/n9/win25.out dump=../n9/sol26.npz tightout=../n9/tight26.txt > ../n9/run26.log 2>&1
mv l2_x_w_dump.txt ../n9/l2_r26.txt; mv l2_x_w_dump.txt.keep l2_x_w_dump.txt
