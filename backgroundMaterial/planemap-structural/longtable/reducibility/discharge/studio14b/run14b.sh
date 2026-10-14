#!/bin/zsh
# the 49 deferred K=1 keys (rings 17-19): dfast18 (11 workers) + 3 ring-17 Lean validations (wheelcheck18), after Job 17
cd "$(dirname $0)"
until [ -f ../studio17/DONE ]; do sleep 60; done
for f in part*.txt; do nice -n 10 ../../wheels/studio/dfast18 $f > ${f%.txt}.out 2>&1 & done
for f in v_a?; do nice -n 10 ../../dcheck/.lake/build/bin/wheelcheck18 $f > $f.lean 2>&1 & done
wait; echo DONE > DONE
