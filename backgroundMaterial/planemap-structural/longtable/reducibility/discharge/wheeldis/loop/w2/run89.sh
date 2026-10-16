#!/bin/bash
# EXPLORE round 16: dfast on the untested d = 8/9 small windows (win89.txt), 3 processes
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win89.txt > x.p$p; done
for p in 0 1 2; do nice -n 5 ../../bin/dfast x.p$p > x.p$p.o 2>&1 & done; wait
cat x.p0.o x.p1.o x.p2.o > win89.out; rm -f x.p? x.p?.o
echo "win89: D $(grep -c D=true win89.out) of $(wc -l < win89.txt)" > run89.log
