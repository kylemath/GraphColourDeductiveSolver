#!/bin/zsh
# Studio Job 3, part c: power controls at n = 24 (stop at the first SAT cubes, no cut log), then n = 26.
cd "$(dirname $0)"
W3=${W3:-8}
run() { echo "START $* $(date)" >> out/progress.txt
        nice -n 10 python3 sat_cubes.py $@ >> out/progress.txt 2>&1
        echo "END $* $(date)" >> out/progress.txt; }
NOCUTLOG=1 STOP_AFTER_SAT=3 run window 24 10 0 2 $W3 1200 out/win_n24_W10_axv0      # power: no axiom, window 10
NOCUTLOG=1 STOP_AFTER_SAT=3 run window 24 10 2 2 $W3 1200 out/win_n24_W10_axv2      # power: anti-A5v, window 10
for w in 10 11 12; do
  run window 26 $w 1 2 $W3 3600 out/win_n26_W${w}_axv1
  grep -q '"status": "SAT"' out/win_n26_W${w}_axv1.jsonl || break
done
NOCUTLOG=1 STOP_AFTER_SAT=1 run closed 24 10 2 2 $W3 1200 out/closed_n24_L10_axv2   # power: anti-A5v closed orbit
echo ALLDONE >> out/progress.txt
