#!/bin/bash
cd "$(dirname "$0")"
export PICYC=./picyc.x
for f in 25 26 27; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-$f.txt out/x$f$m 14 400 --jobx $opt > /dev/null 2>&1; done; done
echo QUEUEX DONE >> out/queueX.log
