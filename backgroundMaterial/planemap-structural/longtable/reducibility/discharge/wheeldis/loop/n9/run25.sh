#!/bin/bash
# EXPLORE round 25: dfast on the 202 untested ring 15-16 windows of the 39 rows round 24 left free
# (binder 559565656/565566666's 11 first, then ring 15, then ring 16), 3-way split, 45-minute wall cap.
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' win25.txt > w.p$p; done
for p in 0 1 2; do timeout 2700 nice -n 5 ../../bin/dfast w.p$p > w.p$p.o 2>&1 & done; wait
cat w.p0.o w.p1.o w.p2.o > win25.out; rm -f w.p? w.p?.o
echo "win25: D $(grep -c D=true win25.out) of $(grep -c ' r=' win25.out) run ($(wc -l < win25.txt) listed)" > run25.log
