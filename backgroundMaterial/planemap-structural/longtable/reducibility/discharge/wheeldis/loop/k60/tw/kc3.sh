#!/bin/sh
# Round 60: kc -C third check on my own triple-wheel windows (isomorphic to TC3_C13/C14/C18), one at a time
cd "$(dirname "$0")"
K=../../kc/kcc
while read -r line; do
  n=$(echo "$line" | cut -d' ' -f1)
  s=$(date -u +%H:%M:%SZ)
  echo "$line" | timeout 5400 $K -C -s 60 -t 3600 > kc_$n.out 2>&1
  echo "$n start $s end $(date -u +%H:%M:%SZ) exit $? : $(tail -1 kc_$n.out)" >> kc3.log
done < tw60_windows.txt
