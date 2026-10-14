#!/bin/zsh
# Job 17: C-reducibility census of wheels (cfast, |X| <= 4, Gonthier admissibility), after Job 14 (12 workers, nice 10)
cd "$(dirname $0)"
# (started directly after Job 14 finished)
nice -n 10 ../studio15/cfast controls.txt --search --limit 5 > controls.out 2>&1
for f in part*.txt; do nice -n 10 ../studio15/cfast $f --search --limit 1000 > ${f%.txt}.out 2>&1 & done
wait; echo DONE > DONE
