#!/bin/bash
# G9: K = 3 complete runs with 8 allowed, centres 6, 7, 8 (one core, nice 10, capped)
cd "$(dirname "$0")"
for c in 6 7 8; do
  s=$(date +%s)
  timeout 900 nice -n 10 ./defectc8 defect_tables8.txt $c 3 1 8 1000000000 200 > g9_K3_c$c.out 2> g9_K3_c$c.err
  echo "centre $c exit $? $(( $(date +%s) - s )) s" >> runK3.log
done
