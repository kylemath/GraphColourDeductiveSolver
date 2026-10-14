#!/bin/zsh
# Studio Job 2 (13 Oct 2026, exploratory): wider gluing. Workers via $W2 (default 2).
cd "$(dirname $0)/.."
W2=${W2:-2}
for spec in "tight33 1500" "glue4 600" "wideB 400" "aimpos 150"; do
  set -- ${=spec}
  nice -n 10 python3 studio_wide.py $1 studio-run/$1.jsonl --limit $2 --workers $W2 > studio-run/$1.log 2>&1
  echo "$1 done $(date)" >> studio-run/progress.txt
done
echo ALLDONE >> studio-run/progress.txt
