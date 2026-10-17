#!/bin/bash
# EXPLORE round 30: the full-registry transfer LP (loop/l2/full_extra.args, now with win29) run long: maxit 60, and no
# iteration starts after 1500 s.  Round 28 did 8 iterations in 368 s; the 2-hour background wall leaves room for one
# long last iteration and the report.  Output moved to n9/l2_r30.txt (l2.py's l2_x_w_dump.txt is restored).
cd "$(dirname "$0")/../l2"
cp l2_x_w_dump.txt l2_x_w_dump.txt.keep
nice -n 5 python3 l2.py maxit=60 tmax=1500 $(cat full_extra.args) dump=../n9/sol30.npz tightout=../n9/tight30.txt > ../n9/run30.log 2>&1
mv l2_x_w_dump.txt ../n9/l2_r30.txt; mv l2_x_w_dump.txt.keep l2_x_w_dump.txt
cp ../n9/run30.log ../n9/run30_iters.txt
