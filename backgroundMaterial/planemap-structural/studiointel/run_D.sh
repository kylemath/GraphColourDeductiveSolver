#!/bin/sh
# studiointel Phase D driver (declared). Waits until (i) the declaration commit $1 is on origin/main and (ii) Phase C has ended; then builds the
# C++ engine, runs both regressions and the hash check (aborting on any failure), then 4 processes at nice 10.
cd "$(dirname "$0")"; DECL=$1; OUT=run-D-2026-10-06; mkdir -p $OUT
until git fetch -q origin main 2>/dev/null && git merge-base --is-ancestor $DECL origin/main; do sleep 60; done
until grep -q '^end' run-C-2026-10-06/runlog.txt 2>/dev/null; do sleep 60; done
echo "declaration $DECL on origin/main, Phase C ended; start $(date '+%F %T')" > $OUT/runlog.txt
shasum -a 256 -c SHA256SUMS >> $OUT/runlog.txt 2>&1 || { echo HASH MISMATCH >> $OUT/runlog.txt; exit 1; }
clang++ -O3 -std=c++17 -o fast/kempe fast/kempe.cpp >> $OUT/runlog.txt 2>&1 || { echo BUILD FAILED >> $OUT/runlog.txt; exit 1; }
nice -n 10 ./regress.sh >> $OUT/runlog.txt 2>&1 || { echo REGRESSION FAILED >> $OUT/runlog.txt; exit 1; }
nice -n 10 python3 fast/regress_fast.py >> $OUT/runlog.txt 2>&1; tail -1 $OUT/runlog.txt | grep -q '^regression passed' || { echo FAST REGRESSION FAILED >> $OUT/runlog.txt; exit 1; }
CAP=200000000
( for sc in A:9=300 A:10=600 A:11=1200 'L(A:3)=900' json:seeds/L-T4.json=600; do s=${sc%=*}; c=${sc##*=}
    nice -n 10 python3 search3.py X --start "$s" --cap-states $CAP --cpu-seconds $c --out $OUT/X1-$(echo "$s" | tr -c 'A-Za-z0-9\n' '_') >> $OUT/X1.out 2>&1; done ) &
nice -n 10 python3 search3.py X --start A:12 --cap-states $CAP --cpu-seconds 3600 --out $OUT/X2 > $OUT/X2.out 2>&1 &
nice -n 10 python3 search3.py C --start json:seeds/C41-r5-8a23ee3e.json --seed 61 --K 6 --cap-states $CAP --cpu-seconds 3600 --out $OUT > $OUT/D61.out 2>&1 &
nice -n 10 python3 search3.py C --start json:seeds/L-T4.json --seed 71 --K 6 --cap-states $CAP --cpu-seconds 3600 --out $OUT > $OUT/D71.out 2>&1 &
wait
echo "end $(date '+%F %T')" >> $OUT/runlog.txt
