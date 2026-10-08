#!/bin/sh
# Track S: Q-run vs R-run lengths on notable holes (R-run >= 6) and the order-33 NR=8 / NR=7 holes. 1 worker, nice 10.
cd "$(dirname "$0")"
while read f rest; do
  nice -n 10 python3 ts_qruns.py ../$f $rest
done < out/notable6.txt > out/qruns_notable.jsonl 2>&1
nice -n 10 python3 ts_qruns.py ../Census33/out/frame-33.txt 'p33.r147#128636:2' 'p33.r115#64736:1' >> out/qruns_notable.jsonl 2>&1
