#!/bin/bash
# EXPLORE round 15: dfast on the untested 8-relaxed windows (win8.txt), 3 processes
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win8.txt > v.p$p; done
for p in 0 1 2; do nice -n 5 ../../bin/dfast v.p$p > v.p$p.o 2>&1 & done; wait
cat v.p0.o v.p1.o v.p2.o > win8.out; rm -f v.p? v.p?.o
echo "win8: D $(grep -c D=true win8.out) of $(wc -l < win8.txt)" > run8.log
