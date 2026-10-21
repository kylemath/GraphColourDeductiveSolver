#!/bin/sh
# Round 60: after kcb2.sh, our kc -C on batch 3's 2 containment survivors, with pair60 paused meanwhile (3 cores)
cd "$(dirname "$0")/../in60"
until grep -q '^# done' kc_b2.log 2>/dev/null; do sleep 15; done
kill -STOP 6018
while read -r line; do
  n=$(echo "$line" | cut -d' ' -f1)
  echo "$line" | timeout 3000 ../../kc/kcc -C -s 60 -t 2400 > kc_$n.out 2>&1
  echo "kc $n $(date -u +%H:%M:%SZ): $(tail -1 kc_$n.out)" >> kc_b3.log
done < cand_b3.txt
kill -CONT 6018
echo "# done $(date -u +%H:%M:%SZ), pair60 resumed" >> kc_b3.log
