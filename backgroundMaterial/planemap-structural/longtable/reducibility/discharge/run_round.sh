#!/bin/zsh
# B8: run dfast on out/parts/$1_{0..3}.txt in 4 niced processes; results to out/dres-$1.txt
cd "$(dirname $0)"
for i in 0 1 2 3; do nice -n 10 ./dfast out/parts/$1_$i.txt > out/parts/$1_$i.out 2>&1 & done
wait; cat out/parts/$1_*.out > out/dres-$1.txt; echo DONE
