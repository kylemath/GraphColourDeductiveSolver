#!/bin/bash
# EXPLORE round 25 tail: the 17 ring-16 windows round 25's cap did not reach, 2 cores (round 26's LP holds the third).
cd "$(dirname "$0")"
for p in 0 1; do awk -v p=$p 'NR%2==p' win25b.txt > wb.p$p; done
for p in 0 1; do timeout 2400 nice -n 5 ../../bin/dfast wb.p$p > wb.p$p.o 2>&1 & done; wait
cat wb.p0.o wb.p1.o > win25b.out; rm -f wb.p? wb.p?.o
