#!/bin/bash
# s86 10 Nov 04:30Z: retry an upperR2 check that was OOM-killed (no verdict). Waits for RFREE MB (default 3200) of memcg free on 3
# samples in a row (20 s apart), then runs U86.sh (same tag, so file86 files a FEASIBLE log); retries up to RTRY times.
# usage: (env of watch86e: STACK ARGS KEYS E86OVR XF) bash rechk86.sh <tag> <sol>
N=$(cd $(dirname $0) && pwd); TG=$1; SOL=$2; RF=${RFREE:-3200}; CGM=/sys/fs/cgroup/memory$(awk -F: '$2=="memory"{print $3}' /proc/self/cgroup)
fr() { echo $(( ($(cat $CGM/memory.limit_in_bytes) - $(awk '$1=="total_rss"{print $2}' $CGM/memory.stat)) / 1048576 )); }
for try in $(seq 1 ${RTRY:-6}); do
  ok=0; while [ $ok -lt 3 ]; do [ $(fr) -ge $RF ] && ok=$((ok+1)) || ok=0; sleep 20; done
  echo "$(date -u +%H:%M:%SZ) [s86RC-$TG] try $try: $(fr) MB free -> U86" >> $N/run.log
  U86_MINFREE_MB=$RF bash $N/U86.sh $TG $SOL 1 $XF
  grep -q '^UPPER-R2: ' $N/logs/upper_$TG.log && { echo "$(date -u +%H:%M:%SZ) [s86RC-$TG] verdict: $(grep '^UPPER-R2: ' $N/logs/upper_$TG.log | tail -1 | cut -c1-120)" >> $N/run.log; exit 0; }
  sleep 300
done
echo "$(date -u +%H:%M:%SZ) [s86RC-$TG] gave up after ${RTRY:-6} tries" >> $N/run.log
