#!/bin/bash
# EXPLORE round 29: dfast on the 16 untested ring <= 16 windows of round 28 binders (bind28.txt), 3 cores, 20-minute cap.
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win29.txt > w.p$p; done
for p in 0 1 2; do timeout 1200 nice -n 5 ../../bin/dfast w.p$p > w.p$p.o 2>&1 & done; wait
cat w.p0.o w.p1.o w.p2.o > win29.out; rm -f w.p? w.p?.o
cd ../w2 && python3 w2.py cover ds=7,9 ../n9/bind28.txt > ../n9/cov29.txt 2>&1
