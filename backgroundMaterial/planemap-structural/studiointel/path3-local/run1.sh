#!/bin/sh
# Round 1: 6 workers x 20 min wall, nice 10 (MacBook rule: <= 6 cores, <= 30 min per run). K=8 candidates/step, KT=4 targeted.
cd "$(dirname "$0")"; O=run1; mkdir -p $O
LT=../../longtable/historical-traps; RC=../run-C-2026-10-06/cert; W=1200
nice -n 10 python3 kc_search_local.py $LT/hog1152-heawood-four-color-graph.json 11 8 4 $W $O 9 hog1152 > $O/hog1152.out 2>&1 &
nice -n 10 python3 kc_search_local.py $LT/heawood1890.json 12 8 4 $W $O 9 heawood1890 > $O/heawood1890.out 2>&1 &
nice -n 10 python3 kc_search_local.py $RC/80b930d1540e4ee3.graph.json 13 8 4 $W $O 9 r5_80b930d1 > $O/r5_80b930d1.out 2>&1 &
nice -n 10 python3 kc_search_local.py $RC/91a307d1852a1764.graph.json 14 8 4 $W $O 9 r5_91a307d1 > $O/r5_91a307d1.out 2>&1 &
nice -n 10 python3 kc_search_local.py build/core/RAK_a13_b1_s2.json 15 8 4 $W $O 9 RAK_a13_b1_s2 > $O/RAK_a13_b1_s2.out 2>&1 &
nice -n 10 python3 kc_search_local.py build/core/FL_n12.json 16 8 4 $W $O 12 FL_n12 > $O/FL_n12.out 2>&1 &
wait
