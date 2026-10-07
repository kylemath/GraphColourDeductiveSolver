#!/bin/bash
cd "$(dirname "$0")"
export PICYC=./picyc.q
for f in 25 26; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-$f.txt out/q$f$m 6 200 --jobq $opt > /dev/null 2>&1; done; done
for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-27.txt out/r27$m 10 400 --jobk --jobm --jobn --jobo --jobp --jobq $opt > /dev/null 2>&1; done
echo QUEUER DONE >> out/queueR.log
