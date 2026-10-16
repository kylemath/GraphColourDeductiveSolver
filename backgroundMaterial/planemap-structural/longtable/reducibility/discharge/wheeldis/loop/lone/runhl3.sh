#!/bin/bash
# EXPLORE round 8: dfast (ring <= 16) on hl3.txt, 2 processes
cd "$(dirname "$0")"
awk 'NR%2==1' hl3.txt > hl3.p0; awk 'NR%2==0' hl3.txt > hl3.p1
nice -n 4 ../../bin/dfast hl3.p0 > hl3.p0.o 2>&1 & p=$!
nice -n 4 ../../bin/dfast hl3.p1 > hl3.p1.o 2>&1; wait $p
cat hl3.p0.o hl3.p1.o > hl3.out; rm -f hl3.p0 hl3.p1 hl3.p0.o hl3.p1.o
echo "hl3: D $(grep -c D=true hl3.out) of $(wc -l < hl3.txt)" >> iter.log
