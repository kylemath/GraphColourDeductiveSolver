# swap17b (10 Nov 00:10Z): IT0 from the env (GS16 iter 1 already ended); GS17 in-point = the lowest-t of GS16's in.json and every
# Mac point macinject logged FEASIBLE on GS16's family + keys (ST-94 0.014859 at 00:08Z).
# s86 (9 Nov 23:30Z, Lead 22:59Z option A): GS16 -> GS17 (357 keys, trimmed warm) + GL18 beside it, at GS16's next natural restart =
# the end of GS16's current iteration (iter line in K.log + its lpdual filed), once (1) the 357-key test chain passed (writes
# p8test/VERDICT_357) and (2) the re-queued ST-92 inject check (macinject86p8c) has a verdict.  GL18 starts only after GS17's first LP
# solve if the memcg then has >= 6.5 GB free (GL ~4 GB + one 2.5 GB check); else it logs that GL does not fit and stops.
N=/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
CGM=/sys/fs/cgroup/memory$(awk -F: '$2=="memory"{print $3}' /proc/self/cgroup 2>/dev/null)
log() { echo "$(date -u +%H:%M:%SZ) [s86SW] $*" >> $N/run.log; }
freemb() { echo $(( ($(cat $CGM/memory.limit_in_bytes) - $(awk '$1=="total_rss"{print $2}' $CGM/memory.stat)) / 1048576 )); }
IT0=${IT0:-$(grep -c '^iter ' $N/runK_k86GS16/K.log)}; log "armed: GS16 at $IT0 finished iterations; waiting for the 357 tests, the ST-92 inject verdict and GS16's next iteration end"
until [ -s $N/p8test/tests7.out ]; do sleep 30; done
if [ $(grep -c PASS $N/p8test/tests7.out) -eq 4 ] && ! grep -v ' 0 tracebacks' $N/p8test/tests7.out | grep -q .; then
  echo "P357OK $(date -u +%H:%M:%SZ) 357 keys p1r/cg_keys_r13w16_16fikpqrstw.txt (449bf4dd = 347 0a66b3c0 + W6b-16w 32b2adae) on eng_p8 / eng_p8l, K3gB5n" > $N/p8test/VERDICT_357
  cat $N/p8test/tests7.out >> $N/p8test/VERDICT_357; log "357-key tests PASS -> p8test/VERDICT_357"
else log "357-key tests NOT all PASS ($(tr '\n' ' ' < $N/p8test/tests7.out | cut -c1-300)); no swap"; exit 1; fi
until grep -q "\[s86MI-k86GS16\] sol_repK1MW_08__K3l5j_k260 (t [0-9.]*\( < t_in [0-9.]*\)\?) \(FEASIBLE\|UPPER-R2\)" $N/run.log; do sleep 30; pgrep -f 'pcheck.py solveR2.*tag=k86GS1[6] ' > /dev/null || break; done
while pgrep -f 'pcheck.py solveR2.*tag=k86GS1[6] ' > /dev/null; do
  n=$(grep -c '^iter ' $N/runK_k86GS16/K.log); [ "$n" -gt "$IT0" ] && break; sleep 30; done
sleep 120   # the lpdual copier and watch86e pick up the iteration's files
GT=$(grep -o "in-point: t_in = [0-9.]*" $N/runK_k86GS16/K.log | tail -1 | grep -o "[0-9.]*$")
FEAS17=$N/eng_p8/sol_k86GS16_in.json; FT=${GT:-9}
for b in $(grep -o "\[s86MI-k86GS16\] [A-Za-z0-9_]* (t [0-9.]* < t_in [0-9.]*) FEASIBLE" $N/run.log | awk '{print $2}' | sort -u); do
  t=$(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['t'])" $N/cand/$b.json 2>/dev/null) || continue
  python3 -I -c "import sys; sys.exit(0 if float(sys.argv[1]) < float(sys.argv[2]) else 1)" $t $FT && { FEAS17=$N/cand/$b.json; FT=$t; }
done
cp $N/runK_k86GS16/K.log $N/logs/K_k86GS16_final.log
for p in $(pgrep -f 'runK86p8.sh 200 2 k86GS1[6] '); do kill $p; done; sleep 1
for p in $(pgrep -f 'pcheck.py solveR2.*tag=k86GS1[6] '); do kill $p; done
for p in $(pgrep -f 'repladder_e.py k86GS1[6] '); do pp=$(ps -o ppid= -p $p | tr -d ' '); kill $p; grep -q relaunch_ladder /proc/$pp/cmdline 2>/dev/null && kill $pp; done
for p in $(pgrep -f '(watch86e|file86|subchk86p8|macinject86p8c|macinject86p8b)\.sh k86GS1[6]$'); do kill $p; done
for p in $(pgrep -f 'lpdual_k86GS1[6]_'); do kill $p; done
for p in $(pgrep -f 'launch_k86GS1[6]\.sh'); do kill $p; done
sleep 3; log "stopped k86GS16 at $(grep -c '^iter ' $N/logs/K_k86GS16_final.log) iterations (t_in ${GT:-?}); GS17 in-point $(basename $FEAS17) (t $(python3 -I -c "import json,sys; print(json.load(open(sys.argv[1]))['t'])" $FEAS17))"
cd $N && FEAS17=$FEAS17 bash $N/launch_k86GS17.sh > $N/logs/launch_k86GS17.out 2>&1 || { log "launch_k86GS17 failed: $(tail -2 $N/logs/launch_k86GS17.out | tr '\n' ' ')"; exit 2; }
until grep -q "lpmax:\|^iter 0" $N/runK_k86GS17/K.log 2>/dev/null; do sleep 30; pgrep -f 'pcheck.py solveR2.*tag=k86GS1[7] ' > /dev/null || { log "GS17 died before its first LP"; exit 3; }; done
sleep 300; fr=$(freemb); rs=$(ps -o rss= -p $(pgrep -f 'pcheck.py solveR2.*tag=k86GS1[7] ' | head -1) | awk '{printf "%d", $1/1024}')
if [ "$fr" -ge 6500 ]; then cd $N && bash $N/launch_k86GL18.sh > $N/logs/launch_k86GL18.out 2>&1; log "GS17 at ${rs} MB, ${fr} MB free -> launched GL18 ($(tail -1 $N/logs/launch_k86GL18.out | cut -c1-120))"
else log "GS17 at ${rs} MB, only ${fr} MB free (< 6500): GL18 NOT started (does not fit beside GS17 + a check)"; fi
