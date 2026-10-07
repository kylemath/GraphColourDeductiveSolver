#!/bin/bash
cd "$(dirname "$0")"
export PICYC=./picyc.e
for f in 24 25 26; do
  nice -n 10 python3 run.py in-plantri-$f.txt out/e$f 6 200 --jobe > /dev/null 2>&1
  nice -n 10 python3 run.py in-plantri-$f.txt out/e${f}m 6 200 --jobe --mirror > /dev/null 2>&1
done
echo QUEUEE DONE >> out/queueE.log
