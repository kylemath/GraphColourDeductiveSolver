#!/bin/bash
# exit when: P1.txt line count changes, min POINTS t drops > 2% vs start, 2 h elapsed, free mem < 25 GB, ST-42 new-row hit or batch COMPLETE
O=~/maclane/maclane-k86/outbox; K=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_K5
mint(){ awk '$4=="K3l5i"||$4=="K3l5j"||$4=="K3l5k"||$4=="K3l5l"||$4=="K3l5m"{print $2}' $O/upper/POINTS.txt | sort -g | head -1; }
t0=${T0:-$(mint)}; p0=$(cat $O/lower/P1.txt $O/v2lower/P1.txt 2>/dev/null | grep -c .); c0=$(grep -l COMPLETE $K/results/log_*.txt | wc -l | tr -d ' '); s0=$(date +%s)
while true; do
  p=$(cat $O/lower/P1.txt $O/v2lower/P1.txt 2>/dev/null | grep -c .); [ "$p" != "$p0" ] && { echo P1-CHANGED; tail -2 $O/v2lower/P1.txt; exit 0; }
  t=$(mint); awk -v a=$t -v b=$t0 'BEGIN{exit !(a < b*0.98)}' && { echo "POINT-DROP $t0 -> $t"; tail -3 $O/upper/POINTS.txt; exit 0; }
  [ $(( $(date +%s) - s0 )) -gt 7200 ] && { echo TIMER-2H; exit 0; }
  m=$(vm_stat | awk '/free|inactive|speculative/{s+=$NF} END{print int(s*16384/1e9)}'); [ "$m" -lt 25 ] && { echo "LOWMEM $m GB"; exit 0; }
  n=$(cd $K && python3 newhits.py); [ -n "$n" ] && { echo "K5-NEW-ROW: $n"; exit 0; }
  c=$(grep -l COMPLETE $K/results/log_*.txt | wc -l | tr -d ' '); [ "$c" -gt "$c0" ] && { echo K5-BATCH-COMPLETE; grep -l COMPLETE $K/results/log_*.txt; exit 0; }
  sleep 120
done
