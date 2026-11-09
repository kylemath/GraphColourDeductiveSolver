#!/bin/bash
cd "$(dirname "$0")"
c0=$(python3 status.py | tail -1 | sed 's/.*complete //')
while true; do
  n=$(python3 newhits.py); [ -n "$n" ] && { echo "NEW-ROW-HIT:"; echo "$n"; exit 0; }
  c=$(python3 status.py | tail -1 | sed 's/.*complete //'); [ "$c" != "$c0" ] && { echo BATCH-COMPLETE; python3 status.py; exit 0; }
  grep -q ALLDONE run.log 2>/dev/null && { echo ALLDONE; python3 status.py; exit 0; }
  m=$(vm_stat | awk '/free|inactive|speculative/{s+=$NF} END{print int(s*16384/1e9)}'); [ "$m" -lt 25 ] && { echo "LOWMEM $m GB"; exit 0; }
  sleep 120
done
