#!/bin/bash
# run mixed.py n L mode on the cubes given (f_1 far end), one after another, per-cube limit TL
cd "$(dirname "$0")"
n=$1; L=$2; mode=$3; TL=$4; shift 4
for c in "$@"; do
  CUBE=$c nice -n 10 python3 mixed.py $n $L $mode $TL 2>&1 | grep -E "^cube|status|SOL|pattern"
done
