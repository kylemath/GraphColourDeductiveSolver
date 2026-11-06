#!/bin/zsh
# HCW13R2 two-engine C check: kc -t 600 -C -x {X} and cfast --fixed {X} (Studio kc 07e79fae, cfast de59e72f), nice 10
cd "$(dirname $0)/../../.."   # wheeldis
f=$1; i=0
while IFS=$'\t' read n k x; do
  t=out/job_HCW13R2/eng/$(basename $f .tsv)_$i; echo "$n $k" > $t.in; echo "$n {$x}" > $t.x
  ( nice -n 10 loop/kc/kc -t 600 -C -x $t.x $t.in; echo "//"; nice -n 10 ../studio15/cfast $t.in --fixed "$x" ) > $t.out 2>&1 &
  i=$((i+1)); if [ $((i % 8)) -eq 0 ]; then wait; fi
done < $f; wait
