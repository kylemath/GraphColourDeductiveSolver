#!/bin/bash
# EXPLORE round 8: cfast --search --limit 1 on the H-L3 misses at ring <= 15 (3 processes, 25 min cap)
cd "$(dirname "$0")"
for p in 0 1 2; do awk -v p=$p 'NR%3==p' hl3c.txt > hl3c.p$p; done
for p in 0 1 2; do timeout 1500 nice -n 4 ../../bin/cfast hl3c.p$p --search --limit 1 > hl3c.p$p.o 2>&1 & done; wait
cat hl3c.p0.o hl3c.p1.o hl3c.p2.o > hl3c.cfast; rm -f hl3c.p? hl3c.p?.o
echo "hl3c: C $(grep -c C-REDUCIBLE hl3c.cfast) of $(wc -l < hl3c.txt) (cfast, 25 min cap)" >> iter.log
