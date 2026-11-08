# s86 v2r upper: U86.sh (upperR2 exhaustive with generic keys) on the engine copy eng_v2, for the v2r upper check (flag v2r in the extras).
# usage: [STACK ARGS] KEYS=<gkeys> [CMD=v2rupshow] bash v2r/U86v.sh <tag> <sol> <threads> [extra]      log: v2r/logs/upper_<tag>.log, one line in v2r/logs/runs.txt
# Waits until MemAvailable >= MEMMIN kB (default 3,000,000); nice -n 19; a watchdog stops the run if one process (python or jsepf) exceeds RSSMAX kB
# (default 1,500,000) or both together RSSTOT kB (default 2,200,000), and records the peaks.
B=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp; N=$B/s86_f2b7
export FAM=full KS=0; unset EGK; . $N/env86.sh; N=$N86; E86=$N/eng_v2
TAG=$1; SOL=$2; TH=${3:-1}; shift 3; WK=/tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/v2r/wr86u_$TAG; mkdir -p $WK $N/v2r/logs; cd $E86
while [ $(awk '/MemAvailable/{print $2}' /proc/meminfo) -lt ${MEMMIN:-3000000} ]; do sleep 30; done
L=$N/v2r/logs/upper_$TAG.log; T0=$(date +%s)
echo "$(date -u +%H:%M:%SZ) start upper $TAG (MemAvailable $(awk '/MemAvailable/{print $2}' /proc/meminfo) kB)" >> $N/v2r/logs/runs.txt
nice -n 19 python3 pcheck.py ${CMD:-upperR2} $F $X nomax sol=$SOL $A threads=$TH work=$WK gkeys=$KEYS gkwin gkleaf "$@" > $L 2>&1 &
P=$!; PK=0; PP=0
while kill -0 $P 2>/dev/null; do
  R=$(ps -o rss= --pid $P --ppid $P 2>/dev/null | awk '{s+=$1} END{print s+0}'); [ "$R" -gt "$PK" ] && PK=$R
  R1=$(ps -o rss= --pid $P --ppid $P 2>/dev/null | awk 'BEGIN{m=0} {if ($1>m) m=$1} END{print m+0}'); [ "$R1" -gt "$PP" ] && { PP=$R1; PL=$(grep -v "^ *\[" $L | tail -1 | cut -c1-60); }
  if [ "$R1" -gt ${RSSMAX:-1500000} ] || [ "$R" -gt ${RSSTOT:-2200000} ]; then echo "U86v: RSS $R1 kB (one process) / $R kB (python + jsepf) above ${RSSMAX:-1500000} / ${RSSTOT:-2200000}: stopped" >> $L; pkill -P $P; kill $P; fi
  sleep 3
done
wait $P; rc=$?
echo "U86v: wall $(( $(date +%s) - T0 )) s, peak RSS $PP kB (largest process; after log line: $PL), $PK kB (python + jsepf), exit $rc" >> $L
echo "$(date -u +%H:%M:%SZ) end upper $TAG STACK=$STACK ARGS=$(basename $ARGS) gkeys $(basename $KEYS) $SOL (md5 $(md5sum < $SOL | cut -c1-8)) extra: $*: $(grep 'UPPER-R2' $L | tail -1) | wall $(( $(date +%s) - T0 )) s, peak RSS $PP kB (one process) $PK kB (total), $(grep -c Traceback $L) tracebacks" >> $N/v2r/logs/runs.txt
rm -rf $WK
