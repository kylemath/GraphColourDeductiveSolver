#!/bin/zsh
# B8b: dfast on the 8-centred 2-balls (rings <= 15), 4 niced processes; results b8b/out/dres-c8.txt
cd "$(dirname $0)/out"
for i in 0 1 2 3; do nice -n 10 ../../dfast parts/c8_$i.cfg > parts/c8_$i.out 2>&1 & done
wait; cat parts/c8_*.out > dres-c8.txt; echo DONE
