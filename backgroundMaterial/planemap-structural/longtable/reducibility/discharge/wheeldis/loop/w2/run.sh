#!/bin/bash
# EXPLORE round 14: dfast on the untested small windows (win14.txt), 3 processes
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win14.txt > w.p$p; done
for p in 0 1 2; do nice -n 5 ../../bin/dfast w.p$p > w.p$p.o 2>&1 & done; wait
cat w.p0.o w.p1.o w.p2.o > win14.out; rm -f w.p? w.p?.o
echo "win14: D $(grep -c D=true win14.out) of $(wc -l < win14.txt)" > run.log
