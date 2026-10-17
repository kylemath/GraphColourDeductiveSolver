#!/bin/bash
# EXPLORE round 28: the transfer LP with the full registry (j28_12.args plus every .out with a D verdict that it lacks,
# loop/l2/full_extra.args).  tmax = 1500 s (no iteration starts after 25 minutes), maxit = 8, so the last iteration
# (about 23 minutes in round 26) and the report fit inside the hour.  l2.py names its output l2_x_w_dump.txt in loop/l2
# (committed from round 24), so it is moved to n9/l2_r28.txt and restored.
cd "$(dirname "$0")/../l2"
cp l2_x_w_dump.txt l2_x_w_dump.txt.keep
nice -n 5 python3 l2.py maxit=8 tmax=1500 $(cat full_extra.args) dump=../n9/sol28.npz tightout=../n9/tight28.txt > ../n9/run28.log 2>&1
mv l2_x_w_dump.txt ../n9/l2_r28.txt; mv l2_x_w_dump.txt.keep l2_x_w_dump.txt
cp ../n9/run28.log ../n9/run28_iters.txt
