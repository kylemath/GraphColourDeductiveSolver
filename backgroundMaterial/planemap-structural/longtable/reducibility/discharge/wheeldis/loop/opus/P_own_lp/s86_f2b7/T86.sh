# s86 T86 (9 Nov, eng_p8 tests): U86.sh with the pcheck command in T86CMD (default upperR2); SOL "-" passes no sol=. The command line carries
# note="pcheck.py upperR2" so U86 waiters count this test as a check (one check at a time, memcg gate). usage: as U86.sh
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; WK=$SD/wr86u_$TAG; mkdir -p $WK $N/logs; cd $E86
echo 900 > /proc/self/oom_score_adj 2>/dev/null   # s86 9 Nov 09:50Z: a check is the first OOM victim, never the LP runs (memcg limit 14.3 GB)
# s86 9 Nov 11:15Z check slot: at most U86_MAXCHK (1) upperR2 checks at once, and only with U86_MINFREE_MB (2500) of the memcg limit
# free (total_rss, not /proc/meminfo); a lock dir serialises the start; after U86_MAXWAIT s (7200) a check starts anyway.
CGM=/sys/fs/cgroup/memory$(awk -F: '$2=="memory"{print $3}' /proc/self/cgroup 2>/dev/null); LK=$N/.u86slot
slot() {
  n=$(pgrep -fc 'pcheck.py upperR2' 2>/dev/null); n=${n:-0}   # (pgrep -c prints 0 and exits 1 when none)
  [ "$n" -lt "${U86_MAXCHK:-1}" ] || return 1
  if [ -r $CGM/memory.stat ] && [ -r $CGM/memory.limit_in_bytes ]; then
    fr=$(( $(cat $CGM/memory.limit_in_bytes) - $(awk '$1=="total_rss"{print $2}' $CGM/memory.stat) ))
    [ $fr -ge $(( ${U86_MINFREE_MB:-2500} * 1048576 )) ] || return 1
  fi
  return 0
}
# s86 9 Nov 12:50Z FIFO: each waiter holds a ticket $N/.u86q/<ns>_<pid>; only the oldest live ticket may take the slot (a ladder that
# queues its next check at once no longer starves the others); tickets of dead pids are pruned.
Q=$N/.u86q; mkdir -p $Q; TK=$Q/$(date +%s%N)_$$; : > $TK; trap 'rm -f $TK' EXIT
first() {
  for f in $(ls $Q 2>/dev/null | sort); do kill -0 ${f##*_} 2>/dev/null && { [ "$Q/$f" = "$TK" ]; return; }; rm -f "$Q/$f"; done; return 0; }
t0=$(date +%s); waited=0
while true; do
  [ -d $LK ] && [ -n "$(find $LK -maxdepth 0 -mmin +3 2>/dev/null)" ] && rmdir $LK 2>/dev/null   # stale lock
  if { first || [ $(( $(date +%s) - t0 )) -ge ${U86_MAXWAIT:-7200} ]; } && mkdir $LK 2>/dev/null; then
    if slot || [ $(( $(date +%s) - t0 )) -ge ${U86_MAXWAIT:-7200} ]; then break; fi
    rmdir $LK
  fi
  waited=1; sleep 20
done
[ $waited = 1 ] && echo "$(date -u +%H:%M:%SZ) [s86U-$TAG] slot after $(( $(date +%s) - t0 )) s wait" >> $N/run.log
nice -n 12 python3 pcheck.py ${T86CMD:-upperR2} $F $X nomax $( [ "$SOL" = - ] || echo sol=$SOL ) "note=pcheck.py upperR2" $A threads=$TH work=$WK gkeys=$KEYS gkwin gkleaf "$@" > $N/logs/t86_$TAG.log 2>&1 &
PC=$!; rm -f $TK; sleep 20; rmdir $LK 2>/dev/null; wait $PC
echo "$(date -u +%H:%M:%SZ) [s86U-$TAG] STACK=$STACK ARGS=$(basename $ARGS) gkeys $(basename $KEYS) $SOL (md5 $(md5sum < $SOL | cut -c1-8)) extra: $*: $(grep -E 'UPPER-R2|SELFTEST:|GKWINTEST:|P8REFTEST:' $N/logs/t86_$TAG.log | tail -1) $(grep -c Traceback $N/logs/t86_$TAG.log) tracebacks" >> $N/run.log
rm -rf $WK
