#!/bin/bash
# [exploratory] Kempe-radius census, plantri -m5 -c4, orders 12..MAX, 8 workers at nice 10.
cd "$(dirname "$0")"
P=$HOME/studio-scratch/plantri-src/plantri58/plantri
MAX=${MAX:-26}
for n in $(seq 12 2 $MAX) ; do :; done
for n in $(seq 12 $MAX); do
  [ -s summary-$n.json ] && continue
  t0=$(date +%s)
  $P -m5 -c4 $n -a 2>/dev/null | nice -n 10 python3 census.py $n out-$n.jsonl --workers 8 > summary-$n.tmp && mv summary-$n.tmp summary-$n.json
  echo "$(date '+%F %T') order $n done in $(( $(date +%s) - t0 )) s: $(cat summary-$n.json)" >> census.log
done
echo "$(date '+%F %T') CENSUS DONE to $MAX" >> census.log
