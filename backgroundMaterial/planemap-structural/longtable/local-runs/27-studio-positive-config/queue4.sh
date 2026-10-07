#!/bin/bash
# per-class orientation check + Job C: orders 12-26, both orientations, with the class-signature engine
cd "$(dirname "$0")"
while ! grep -q "QUEUE3 DONE" out/queue3.log 2>/dev/null; do sleep 30; done
export PICYC=./picyc.new
for f in 12-23 24 25 26; do
  nice -n 10 python3 run.py in-plantri-$f.txt out/c$f 12 200 --full > /dev/null 2>&1
  nice -n 10 python3 run.py in-plantri-$f.txt out/c${f}m 12 200 --full --mirror > /dev/null 2>&1
done
echo QUEUE4 DONE >> out/queue4.log
