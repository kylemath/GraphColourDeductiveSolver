#!/bin/bash
# G9 probe 2: K = 3 capped runs, centres 9..12 (one core, nice 10)
cd "$(dirname "$0")"
for c in 9 10 11 12; do
  s=$(date +%s)
  timeout ${CAP:-150} nice -n 10 ./defectc9 defect_tables9.txt $c 3 1 8 1000000000 200 > big_K3_c$c.out 2> big_K3_c$c.err
  echo "centre $c exit $? $(( $(date +%s) - s )) s" >> runbig.log
done
