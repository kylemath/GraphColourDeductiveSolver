#!/bin/bash
cd "$(dirname "$0")"
while ! grep -q "QUEUEG DONE" out/queueG.log 2>/dev/null; do sleep 15; done
export PICYC=./picyc.h
for f in 24 25 26; do
  nice -n 10 python3 run.py in-plantri-$f.txt out/h$f 10 200 --jobh > /dev/null 2>&1
  nice -n 10 python3 run.py in-plantri-$f.txt out/h${f}m 10 200 --jobh --mirror > /dev/null 2>&1
done
mkdir -p out/hpos
grep -v -- '--mirror' out/fpos/jobs.txt | sed 's/ *$//' | while read fn hs; do nice -n 10 ./picyc.h $fn --jobh --holes $hs > out/hpos/$(basename ${fn%.in}).out; done
grep -- '--mirror' out/fpos/jobs.txt | while read fn hs mir; do nice -n 10 ./picyc.h $fn --jobh --holes $hs --mirror > out/hpos/$(basename ${fn%.in}).out; done
cat out/hpos/*.out > out/hpos.jsonl
echo QUEUEH DONE >> out/queueH.log
