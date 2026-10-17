#!/bin/bash
# EXPLORE round 27: dfast on the 16 untested ring <= 16 windows of round 25/26's binders (bind25.txt), 3 cores, 30-minute cap.
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win27.txt > w.p$p; done
for p in 0 1 2; do timeout 1800 nice -n 5 ../../bin/dfast w.p$p > w.p$p.o 2>&1 & done; wait
cat w.p0.o w.p1.o w.p2.o > win27.out; rm -f w.p? w.p?.o
cd ../w2 && python3 w2.py cover ds=7,10 ../n9/bind25.txt > ../n9/cov27.txt 2>&1
