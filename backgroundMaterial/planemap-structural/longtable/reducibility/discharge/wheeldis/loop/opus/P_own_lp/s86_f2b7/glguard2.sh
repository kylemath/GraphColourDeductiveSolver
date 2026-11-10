# s86 (9 Nov 23:20Z, after GL17's 22:56Z OOM lesson): GS checks have priority (Lead 20:30Z / 22:59Z).  usage: bash glguard2.sh <GL tag>
# Every 10 s: if an upperR2 check (or a T86 test) runs and the memcg has < GLG_MINFREE_MB (1200) free, or a U86 ticket waited > 20 min
# with < 2.5 GB free, snapshot the GL run's rows (warm/rows_<tag>_snap_guard.txt) and stop it + its helpers.  Exits when the GL run is gone.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
T=$1; P="${T%?}[${T: -1}]"; CGM=/sys/fs/cgroup/memory$(awk -F: '$2=="memory"{print $3}' /proc/self/cgroup 2>/dev/null)
while pgrep -f "pcheck.py solveR2.*tag=$P " > /dev/null; do
  fr=$(( ($(cat $CGM/memory.limit_in_bytes) - $(awk '$1=="total_rss"{print $2}' $CGM/memory.stat)) / 1048576 ))
  old=$(find $N/.u86q -type f -mmin +20 2>/dev/null | wc -l); chk=$(pgrep -fc 'pcheck.py (upperR2|p8reftest|gkwintest|p1rordtest)'); chk=${chk:-0}
  why=""
  [ "$chk" -gt 0 ] && [ "$fr" -lt ${GLG_MINFREE_MB:-1200} ] && why="a check runs with ${fr} MB free"
  [ "$old" -gt 0 ] && [ "$fr" -lt 2500 ] && why="a check waited > 20 min with ${fr} MB free"
  if [ -n "$why" ]; then
    python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p8l/rows_$T.txt $N/warm/rows_${T}_snap_guard.txt 2>/dev/null
    for p in $(pgrep -f "runK86p8l.sh 200 2 $P "); do kill $p; done; sleep 1
    for p in $(pgrep -f "pcheck.py solveR2.*tag=$P "); do kill $p; done
    for p in $(pgrep -f "(watchL86p8l|dualwatch86p8l|bindwatch86).sh $P\$"); do kill $p; done
    echo "$(date -u +%H:%M:%SZ) [s86G] glguard2: $why -> stopped $T (rows -> warm/rows_${T}_snap_guard.txt, $(wc -l < $N/warm/rows_${T}_snap_guard.txt 2>/dev/null) lines)" >> $N/run.log
    exit 0
  fi
  sleep 10
done
