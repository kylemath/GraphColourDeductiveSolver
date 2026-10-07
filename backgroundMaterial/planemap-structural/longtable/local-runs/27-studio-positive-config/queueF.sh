#!/bin/bash
cd "$(dirname "$0")"
export PICYC=./picyc.f
for f in 24 25 26; do
  nice -n 10 python3 run.py in-plantri-$f.txt out/f$f 6 200 --sigc > /dev/null 2>&1
  nice -n 10 python3 run.py in-plantri-$f.txt out/f${f}m 6 200 --sigc --mirror > /dev/null 2>&1
done
echo QUEUEF DONE >> out/queueF.log
