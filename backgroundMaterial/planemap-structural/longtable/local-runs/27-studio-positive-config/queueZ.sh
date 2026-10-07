#!/bin/bash
cd "$(dirname "$0")"
while ! grep -q "QUEUEX DONE" out/queueX.log 2>/dev/null; do sleep 15; done
export PICYC=./picyc.z
for f in 25 26 27; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-$f.txt out/z$f$m 14 400 --jobz $opt > /dev/null 2>&1; done; done
echo QUEUEZ DONE >> out/queueZ.log
