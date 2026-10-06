#!/bin/bash
# [exploratory] Kempe-class multiplicity census, orders 12..MAX, 6 workers at nice 10.
cd "$(dirname "$0")"
P=$HOME/studio-scratch/plantri-src/plantri58/plantri
for n in 12 14 15 16 17 18 19 20 21 22 23 24 25 26; do
  [ -s kc-summary-$n.json ] && continue
  t0=$(date +%s)
  $P -m5 -c4 $n -a 2>/dev/null | nice -n 10 python3 kcensus.py $n kc-$n.jsonl --workers 6 > kc-summary-$n.tmp && mv kc-summary-$n.tmp kc-summary-$n.json
  echo "$(date '+%F %T') kc order $n done in $(( $(date +%s) - t0 )) s" >> kcensus.log
done
echo "$(date '+%F %T') KCENSUS DONE" >> kcensus.log
