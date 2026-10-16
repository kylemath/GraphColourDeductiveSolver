#!/bin/bash
# EXPLORE round 7: ring-16 dfast on u10.txt (receiver-free) then b10.txt (B-fixed, d = 9/11/12), 3 processes
cd "$(dirname "$0")"
for k in u10 b10; do
  for p in 0 1 2; do awk -v p=$p 'NR%3==p' $k.txt > $k.p$p; done
  for p in 0 1 2; do nice -n 5 ../../bin/dfast $k.p$p > $k.p$p.o 2>&1 & done; wait
  cat $k.p0.o $k.p1.o $k.p2.o > $k.out; rm -f $k.p? $k.p?.o
  echo "$k: D $(grep -c D=true $k.out) of $(wc -l < $k.txt)" >> iter.log
done
python3 ufree.py mkpat u10.out u10.pat 17 > /dev/null; echo "run16 done" >> iter.log
