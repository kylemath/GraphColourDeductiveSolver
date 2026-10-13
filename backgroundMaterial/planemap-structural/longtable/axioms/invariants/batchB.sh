#!/bin/bash
# windows without axiom (axv=0) and anti (axv=2), word 1212
cd "$(dirname "$0")"
for a in "18 7 0 100000 600" "20 9 0 100000 850" "16 6 0 100000 300" "18 6 0 5000 600" "20 8 0 3000 850" "18 6 2 100000 300"; do
  set -- $a
  nice -n 10 python3 enum_win.py $1 $2 $3 $4 $5 data/win_n$1_W$2_axv$3.jsonl
done
