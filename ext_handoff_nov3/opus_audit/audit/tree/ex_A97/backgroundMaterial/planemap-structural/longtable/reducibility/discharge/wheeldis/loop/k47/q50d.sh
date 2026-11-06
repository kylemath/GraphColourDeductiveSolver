# Round 50 queue, part 3 (replaces q50b/q50c, Long Table 23:27Z: the main-line d = 7 row goes ahead of d = 10).
# Finish the d = 9 656656665 row (driver PID $1); growth census of d = 7 7665566/6675666 (= the main line's
# 7665566/6665766 reflected); its ring 15-16 sweep; then the d = 10 row.  3 cores at most.
cd "$(dirname "$0")"
while kill -0 $1 2>/dev/null; do sleep 20; done
python3 minkill47.py win45_9_656656665_665555555_A14.txt 656656665 r9d; date -u +%H:%MZ; cat r9d_kills_min.txt; touch R50C.DONE
TW=/tmp/claude-0/-home-claude/e93ccb28-7843-5c35-aaad-eabd09ceeb9b/scratchpad/tw
(cd $TW && python3 out/job30/twoeng.py | tail -1)
python3 ../k50/census50.py 7 7665566 6675666 $TW/out/job30/k3x_D.out $TW/out/job30/k3x_C.cfast; date -u +%H:%MZ; touch CEN50.DONE
W=win45_7_7665566_6675666_A16.txt
[ -f $W ] || python3 win45.py 16 7 7665566 6675666
date -u +%H:%MZ; wc -l < $W
STOP=0 NW=3 python3 drive45.py $W 600 > drive50_r7d16.log 2>&1
python3 minkill47.py $W 7665566 r7d16; date -u +%H:%MZ; cat r7d16_kills_min.txt; touch R50E.DONE
W=win45_10_6556656556_6665656665_A14.txt
[ -f $W ] || python3 win45.py 14 10 6556656556 6665656665
python3 - $W <<'PY'
import sys
w = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
done = {l.split()[0] for l in open('A_kcc.out') if l[:1] == 'a'}; k = {l.split()[0] for l in open('KILL')}
print('%s: %d windows, %d already run, %d already two-engine kills' % (sys.argv[1], len(w), sum(x in done for x in w), sum(x in k for x in w)))
PY
date -u +%H:%MZ
STOP=0 NW=3 python3 drive45.py $W 600 > drive50_r10a.log 2>&1
python3 minkill47.py $W 6556656556 r10a; date -u +%H:%MZ; cat r10a_kills_min.txt; touch R50D.DONE
grep -c MISMATCH A_df.out A_cf.out KILL
