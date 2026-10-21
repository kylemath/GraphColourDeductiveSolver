#!/bin/sh
# Round 60: our kc -C on the other thread's 10 TC3 lines (data copy in in/), then our dfast on every kc D, one at a time
cd "$(dirname "$0")"
while read -r line; do
  n=$(echo "$line" | cut -d' ' -f1)
  echo "$line" | timeout 3600 ../../kc/kcc -C -s 60 -t 3000 > kc_$n.out 2>&1
  echo "kc $n: $(tail -1 kc_$n.out)" >> kc3b.log
done < in/tc3_all.txt
cat tw60_windows.txt in/tc3_all.txt > all13.txt
while read -r line; do
  n=$(echo "$line" | cut -d' ' -f1)
  if grep -q 'D=true' kc_$n.out; then
    echo "$line" > df_$n.txt
    s=$(date -u +%H:%M:%SZ)
    timeout 3600 ../../../bin/dfast df_$n.txt > df_$n.out 2>&1
    echo "dfast $n ($s-$(date -u +%H:%M:%SZ)): $(tail -1 df_$n.out)" >> kc3b.log
  fi
done < all13.txt
echo "# done $(date -u +%H:%M:%SZ)" >> kc3b.log
