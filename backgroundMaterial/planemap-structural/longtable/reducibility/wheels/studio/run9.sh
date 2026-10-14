#!/bin/zsh
# Job 9: 2-ball configurations around 66666, rings <= 15, C++ DCheck port (dfast), 10 parts in parallel (nice 10)
cd "$(dirname $0)"
for f in run9/part*.txt; do nice -n 10 ./dfast $f > ${f%.txt}.out 2>&1 & done
wait; echo DONE > run9/DONE
