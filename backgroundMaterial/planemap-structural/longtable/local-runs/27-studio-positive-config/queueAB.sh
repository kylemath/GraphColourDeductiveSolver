#!/bin/bash
cd "$(dirname "$0")"
while ! grep -q "Z DONE" out/queueW.log 2>/dev/null; do sleep 15; done
export PICYC=./picyc.ab
for f in 25 26 27; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-$f.txt out/ab$f$m 14 400 --jobab $opt > /dev/null 2>&1; done; done
echo AB DONE >> out/queueAB.log
