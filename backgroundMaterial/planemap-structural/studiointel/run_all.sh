#!/bin/sh
# studiointel run driver: waits until no wp_shard_runner workers remain, then regress, then Phase A and three Phase B seeds (<=4 processes, nice 10).
cd "$(dirname "$0")"; OUT=run-2026-10-06; mkdir -p $OUT
while [ "$(ps aux | grep -c '[w]p_shard_runner')" -gt 0 ]; do sleep 30; done
echo "start $(date '+%F %T')" > $OUT/runlog.txt
nice -n 10 ./regress.sh >> $OUT/runlog.txt 2>&1 || { echo REGRESSION FAILED >> $OUT/runlog.txt; exit 1; }
shasum -a 256 -c SHA256SUMS >> $OUT/runlog.txt 2>&1
nice -n 10 python3 search.py A --specs 'L(ico),GC:2,A:5,A:6,A:7,A:8,L(A:3)' --cpu-seconds 1200 --out $OUT > $OUT/A.out 2>&1 &
nice -n 10 python3 search.py B --seed 1 --start A:5 --cpu-seconds 1800 --out $OUT > $OUT/B1.out 2>&1 &
nice -n 10 python3 search.py B --seed 2 --start A:6 --cpu-seconds 1800 --out $OUT > $OUT/B2.out 2>&1 &
nice -n 10 python3 search.py B --seed 3 --start 'L(ico)' --cpu-seconds 1800 --out $OUT > $OUT/B3.out 2>&1 &
wait
echo "end $(date '+%F %T')" >> $OUT/runlog.txt
