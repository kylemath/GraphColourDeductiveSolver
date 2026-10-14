#!/bin/zsh
# Studio Job 3 (13 Oct 2026, exploratory): T1-v exact search at n = 24, 26 by cubes. 8 workers, nice 10.
# args of sat_cubes.py: kind n L|W axv depth workers cube_tlimit out
cd "$(dirname $0)"
W3=${W3:-8}
run() { echo "START $* $(date)" >> out/progress.txt
        nice -n 10 python3 sat_cubes.py $@ >> out/progress.txt 2>&1
        echo "END $* $(date)" >> out/progress.txt; }
run window 22  9 1 1 $W3 3600 out/win_n22_W9_axv1     # known UNSAT (Long Table: 392 s uncubed)
run window 24 10 1 2 $W3 3600 out/win_n24_W10_axv1
run window 24  9 1 2 $W3 3600 out/win_n24_W9_axv1
run closed 24 10 1 2 $W3 3600 out/closed_n24_L10_axv1
run closed 24 10 2 2 $W3 1200 out/closed_n24_L10_axv2  # power control (anti-A5v): must find orbits
run window 26 10 1 2 $W3 3600 out/win_n26_W10_axv1
run closed 26 10 1 2 $W3 3600 out/closed_n26_L10_axv1
echo ALLDONE >> out/progress.txt
