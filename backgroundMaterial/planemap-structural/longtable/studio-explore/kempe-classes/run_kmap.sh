#!/bin/bash
# [exploratory] workstream A: kmap census (vertex deg 5/6/7 and edge deletions) orders 21-24, vertex-only 25-26; starts after the kclass census.
cd "$(dirname "$0")"
while kill -0 $(python3 -c "import json;print(json.load(open('kcensus.pid'))['pid'])") 2>/dev/null; do sleep 30; done
P=$HOME/studio-scratch/plantri-src/plantri58/plantri
for n in 21 22 23 24 25 26; do
  [ -s km-done-$n ] && continue
  t0=$(date +%s); X=""; [ $n -ge 25 ] && X="--no-edges"
  $P -m5 -c4 $n -a 2>/dev/null | nice -n 10 python3 kmapcensus.py $n km-$n.jsonl --workers 6 $X > km-done-$n
  echo "$(date '+%F %T') km order $n $X done in $(( $(date +%s) - t0 )) s" >> kmap.log
done
echo "$(date '+%F %T') KMAP DONE" >> kmap.log
