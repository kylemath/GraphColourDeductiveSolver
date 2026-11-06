#!/bin/zsh
# HDW13 three-engine D check: dfast18 (07cb1e0b), cfast (de59e72f), kc -C -s 60 -t 600 (07e79fae); nice 10, 6 at a time
cd "$(dirname $0)/../../.."   # wheeldis
J=out/job_HDW13/eng; i=0
while IFS=$'\t' read n k; do
  t=$J/l$i; echo "$n $k" > $t.in
  ( nice -n 10 out/job52/dfast18 $t.in; nice -n 10 ../studio15/cfast $t.in; nice -n 10 loop/kc/kc -C -s 60 -t 600 $t.in ) > $t.out 2>&1 &
  i=$((i+1)); if [ $((i % 6)) -eq 0 ]; then wait; fi
done < out/job_HDW13/D_w13.tsv; wait; echo ENGDONE > $J/ENGDONE
