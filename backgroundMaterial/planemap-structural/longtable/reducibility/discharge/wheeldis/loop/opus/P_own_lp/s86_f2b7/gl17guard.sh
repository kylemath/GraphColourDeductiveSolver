# s86 (9 Nov 21:15Z): GS16's checks have priority (Lead 20:30Z).  Every minute: if a U86/T86 ticket has waited > 20 min while the memcg
# has < 2.5 GB free, snapshot GL17's rows (warm/rows_k86GL17_snap_guard.txt) and stop GL17 + its helpers.  Exits when GL17 is gone.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
CGM=/sys/fs/cgroup/memory$(awk -F: '$2=="memory"{print $3}' /proc/self/cgroup 2>/dev/null)
while pgrep -f 'pcheck.py solveR2.*tag=k86GL1[7] ' > /dev/null; do
  fr=$(( ($(cat $CGM/memory.limit_in_bytes) - $(awk '$1=="total_rss"{print $2}' $CGM/memory.stat)) / 1048576 ))
  old=$(find $N/.u86q -type f -mmin +20 2>/dev/null | wc -l)
  if [ "$old" -gt 0 ] && [ "$fr" -lt 2500 ]; then
    python3 -c "import sys; b = open(sys.argv[1], 'rb').read(); open(sys.argv[2], 'wb').write(b[:b.rfind(b'\n') + 1])" $N/eng_p8l/rows_k86GL17.txt $N/warm/rows_k86GL17_snap_guard.txt 2>/dev/null
    for p in $(pgrep -f 'runK86p8l.sh 200 2 k86GL1[7] '); do kill $p; done; sleep 1
    for p in $(pgrep -f 'pcheck.py solveR2.*tag=k86GL1[7] '); do kill $p; done
    for p in $(pgrep -f '(watchL86p8l|dualwatch86p8l|bindwatch86).sh k86GL1[7]$'); do kill $p; done
    echo "$(date -u +%H:%M:%SZ) [s86G] gl17guard: a check waited > 20 min with ${fr} MB free -> stopped k86GL17 (rows -> warm/rows_k86GL17_snap_guard.txt, $(wc -l < $N/warm/rows_k86GL17_snap_guard.txt 2>/dev/null) lines)" >> $N/run.log
    exit 0
  fi
  sleep 60
done
