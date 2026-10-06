#!/bin/sh
# studiointel Phase C driver (declared). Waits until the declaration commit $1 is on origin/main, then: regress, hashes, 4 processes at nice 10.
cd "$(dirname "$0")"; DECL=$1; OUT=run-C-2026-10-06; mkdir -p $OUT
until git fetch -q origin main 2>/dev/null && git merge-base --is-ancestor $DECL origin/main; do sleep 60; done
echo "declaration $DECL on origin/main; start $(date '+%F %T')" > $OUT/runlog.txt
nice -n 10 ./regress.sh >> $OUT/runlog.txt 2>&1 || { echo REGRESSION FAILED >> $OUT/runlog.txt; exit 1; }
shasum -a 256 -c SHA256SUMS >> $OUT/runlog.txt 2>&1 || { echo HASH MISMATCH >> $OUT/runlog.txt; exit 1; }
nice -n 10 python3 search2.py X --start 'L(A:3)' --cap-states 1500000 --cpu-seconds 1800 --out $OUT > $OUT/X.out 2>&1 &
nice -n 10 python3 search2.py C --start json:seeds/B2-best.json --seed 21 --K 6 --cpu-seconds 1800 --out $OUT > $OUT/C21.out 2>&1 &
nice -n 10 python3 search2.py C --start json:seeds/B3-best.json --seed 31 --K 6 --cpu-seconds 1800 --out $OUT > $OUT/C31.out 2>&1 &
( nice -n 10 python3 search2.py C --start json:seeds/order28.json --seed 41 --K 6 --cpu-seconds 1200 --out $OUT > $OUT/C41.out 2>&1
  nice -n 10 python3 search2.py C --start json:seeds/T4.json --seed 51 --K 6 --cpu-seconds 600 --out $OUT > $OUT/C51.out 2>&1 ) &
wait
echo "end $(date '+%F %T')" >> $OUT/runlog.txt
