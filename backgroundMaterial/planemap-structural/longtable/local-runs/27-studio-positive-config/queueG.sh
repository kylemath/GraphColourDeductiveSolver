#!/bin/bash
cd "$(dirname "$0")"
while ! grep -q "QUEUEF DONE" out/queueF.log 2>/dev/null; do sleep 15; done
export PICYC=./picyc.g
for f in 25 26; do
  nice -n 10 python3 run.py in-plantri-$f.txt out/g$f 6 200 --jobg > /dev/null 2>&1
  nice -n 10 python3 run.py in-plantri-$f.txt out/g${f}m 6 200 --jobg --mirror > /dev/null 2>&1
done
echo QUEUEG DONE >> out/queueG.log
