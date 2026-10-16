#!/bin/bash
# EXPLORE round 17: dfast on the ring-17 HARD28 windows (win17.txt), 3 processes
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win17.txt > y.p$p; done
for p in 0 1 2; do nice -n 5 ../../bin/dfast y.p$p > y.p$p.o 2>&1 & done; wait
cat y.p0.o y.p1.o y.p2.o > win17.out; rm -f y.p? y.p?.o
echo "win17: D $(grep -c D=true win17.out) of $(wc -l < win17.txt)" > run17.log
