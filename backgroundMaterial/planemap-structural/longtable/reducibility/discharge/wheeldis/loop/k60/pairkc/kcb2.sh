#!/bin/sh
# Round 60: after the r60b pair windows, our kc -C on batch 2's 2 containment survivors, then resume pair60 (SIGCONT)
cd "$(dirname "$0")/../in60"
while kill -0 7624 2>/dev/null; do sleep 15; done
while read -r line; do
  n=$(echo "$line" | cut -d' ' -f1)
  echo "$line" | timeout 3000 ../../kc/kcc -C -s 60 -t 2400 > kc_$n.out 2>&1
  echo "kc $n $(date -u +%H:%M:%SZ): $(tail -1 kc_$n.out)" >> kc_b2.log
done < cand_b2.txt
kill -CONT 6018
echo "# done $(date -u +%H:%M:%SZ), pair60 resumed" >> kc_b2.log
