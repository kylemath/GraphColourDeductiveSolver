#!/bin/bash
# A5v windows (axv=1), word 1212
cd "$(dirname "$0")"
for a in "20 8 1 100000 800" "22 8 1 100000 850" "20 7 1 100000 600" "18 5 1 100000 300" "16 4 1 100000 200" "22 7 1 3000 850" "20 6 1 3000 600" "22 6 1 3000 600"; do
  set -- $a
  nice -n 10 python3 enum_win.py $1 $2 $3 $4 $5 data/win_n$1_W$2_axv$3.jsonl
done
