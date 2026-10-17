#!/bin/bash
# EXPLORE round 24: build the d = 9/10 family and its untested small windows (run from loop/n9).
# tight23.txt and sol23.npz come from:  (cd ../l2 && python3 l2.py maxit=4 pat=loop/w2/win14.out pat=loop/w2/win8.out
#   pat=loop/w2/win89.out dump=../n9/sol23.npz tightout=../n9/tight23.txt)
# Family: rows tight at that solution with d = 9/10 and no 7/8 link vertex.  (A sep3 enumeration of every d = 9/10
# arrangement reaching d - 6 + t timed out at many = 200000, so the LP's tight rows stand in for it.)
cd "$(dirname "$0")"
grep -E 'd=(9|10) ' tight23.txt | awk '$4 !~ /[78]/' > fam9.txt
cd ../w2
for R in 14 15 16; do python3 w2.py build ../n9/win9_r$R.txt $R ../n9/fam9.txt ds=9,10; done
# then: ../n9/run9.sh (dfast on win9_r14.txt), and  python3 w2.py cover ds=9,10 ../n9/fam9.txt > ../n9/cov9.txt
