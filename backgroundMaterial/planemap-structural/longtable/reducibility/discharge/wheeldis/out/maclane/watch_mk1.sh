#!/bin/bash
# exit when the min t of family K3l5j_k260 drops > 2% under T0 (MK1 auto-check trigger; 0.98*T0), or low memory
O=~/maclane/maclane-k86/outbox
while true; do
  t=$(awk '$4=="K3l5j_k260"||$4=="K3l5m_k260"||$4=="K3l5n_k260"||$4=="K3l5q_k260"{print $2}' $O/upper/POINTS.txt | sort -g | head -1)
  [ -n "$t" ] && awk -v a=$t -v b=$T0 'BEGIN{exit !(a < b*0.98)}' && { echo "MK1-POINT-DROP $T0 -> $t"; awk '$4=="K3l5j_k260"' $O/upper/POINTS.txt | tail -3; exit 0; }
  m=$(vm_stat | awk '/free|inactive|speculative/{s+=$NF} END{print int(s*16384/1e9)}'); [ "$m" -lt 25 ] && { echo "LOWMEM $m GB"; exit 0; }
  sleep 120
done
