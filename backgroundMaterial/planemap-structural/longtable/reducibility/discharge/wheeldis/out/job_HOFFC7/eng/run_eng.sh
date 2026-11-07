#!/bin/zsh
# HOFFC7-D engines: dfast18 (07cb1e0b) + kc -C -s 60 -t 600 (07e79fae) on the 53 kc lines, nice 20, 4 at a time
cd "$(dirname $0)/../../.."   # wheeldis
J=out/job_HOFFC7/eng; i=0
while read line; do
  t=$J/l$i; echo "$line" > $t.in
  ( nice -n 20 out/job52/dfast18 $t.in; nice -n 20 loop/kc/kc -C -s 60 -t 600 $t.in ) > $t.out 2>&1 &
  i=$((i+1)); if [ $((i % 4)) -eq 0 ]; then wait; fi
done < $J/D53.kc; wait; echo ENGDONE > $J/ENGDONE
