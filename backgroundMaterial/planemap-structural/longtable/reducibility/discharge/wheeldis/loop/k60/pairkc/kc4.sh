#!/bin/sh
# Round 60: our kc -C on the 4 pair windows of the Formal thread that hold no registry or 2026 configuration
cd "$(dirname "$0")/../in60"
while read -r line; do
  n=$(echo "$line" | cut -d' ' -f1)
  echo "$line" | timeout 3000 ../../kc/kcc -C -s 60 -t 2400 > kc_$n.out 2>&1
  echo "kc $n $(date -u +%H:%M:%SZ): $(tail -1 kc_$n.out)" >> kc4.log
done < cand4.txt
echo "# done $(date -u +%H:%M:%SZ)" >> kc4.log
