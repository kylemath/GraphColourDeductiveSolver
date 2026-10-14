#!/bin/zsh
# Job 8: all wheel instances through the Lean DCheck executable, 12 parts in parallel (nice 10)
cd "$(dirname $0)"
for f in run8/part*.txt; do nice -n 10 ../../dcheck/.lake/build/bin/wheelcheck $f > ${f%.txt}.out 2>&1 & done
wait; echo DONE > run8/DONE
