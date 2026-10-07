#!/bin/sh
# Math C6 adversary run: 6 workers x 25 min wall, nice 10 (coordinator: <= 6 cores, <= 30 min per run, <= 3 CPU-h total). K = 8.
cd "$(dirname "$0")"; O=run_dd; mkdir -p $O; W=1500
LT=../../longtable/historical-traps; RC=../run-C-2026-10-06/cert
nice -n 10 python3 kc_dd_search.py A_5 31 8 $W $O 9 exc A5_exc > $O/A5_exc.out 2>&1 &
nice -n 10 python3 kc_dd_search.py A_6 32 8 $W $O 9 chain A6_chain > $O/A6_chain.out 2>&1 &
nice -n 10 python3 kc_dd_search.py A_7 33 8 $W $O 9 exc A7_exc > $O/A7_exc.out 2>&1 &
nice -n 10 python3 kc_dd_search.py ../path3/seeds/K3_26_5401.json 34 8 $W $O 9 exc K3_exc > $O/K3_exc.out 2>&1 &
nice -n 10 python3 kc_dd_search.py $RC/80b930d1540e4ee3.graph.json 35 8 $W $O 9 exc r5_80b930d1_exc > $O/r5_80b930d1_exc.out 2>&1 &
nice -n 10 python3 kc_dd_search.py $LT/hog1152-heawood-four-color-graph.json 36 8 $W $O 9 chain hog1152_chain > $O/hog1152_chain.out 2>&1 &
wait
