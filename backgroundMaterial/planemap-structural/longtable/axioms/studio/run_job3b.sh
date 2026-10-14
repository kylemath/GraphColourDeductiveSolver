#!/bin/zsh
# Studio Job 3, revised order (Long Table note, 13 Oct): n = 24 window 10 under A5v is decisive (window 9 is
# known SAT); closed L = 10 only if window 10 stalls; anti-A5v power control at n = 24; then n = 26 starting at
# window 10 and going up while SAT.  8 workers, nice 10.
cd "$(dirname $0)"
W3=${W3:-8}
while pgrep -f "sat_cubes.py window 22 9" > /dev/null; do sleep 20; done   # let the n = 22 check finish
run() { echo "START $* $(date)" >> out/progress.txt
        nice -n 10 python3 sat_cubes.py $@ >> out/progress.txt 2>&1
        echo "END $* $(date)" >> out/progress.txt; }
run window 24 10 1 2 $W3 3600 out/win_n24_W10_axv1
grep -q TIMEOUT out/win_n24_W10_axv1.jsonl && run closed 24 10 1 2 $W3 3600 out/closed_n24_L10_axv1
run closed 24 10 2 2 $W3 1200 out/closed_n24_L10_axv2        # power control (anti-A5v): must find orbits
for w in 10 11 12; do
  run window 26 $w 1 2 $W3 3600 out/win_n26_W${w}_axv1
  grep -q '"status": "SAT"' out/win_n26_W${w}_axv1.jsonl || break
done
echo ALLDONE >> out/progress.txt
