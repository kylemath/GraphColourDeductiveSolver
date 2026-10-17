#!/bin/bash
# EXPLORE round 24: dfast on the untested ring <= 14 windows of the d = 9/10 family, 3-way split
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win9_r14.txt > w.p$p; done
for p in 0 1 2; do nice -n 5 ../../bin/dfast w.p$p > w.p$p.o 2>&1 & done; wait
cat w.p0.o w.p1.o w.p2.o > win9.out; rm -f w.p? w.p?.o
echo "win9: D $(grep -c D=true win9.out) of $(wc -l < win9_r14.txt)" > run9.log
