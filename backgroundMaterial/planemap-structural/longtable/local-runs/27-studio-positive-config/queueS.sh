#!/bin/bash
cd "$(dirname "$0")"
while ! grep -q "QUEUER DONE" out/queueR.log 2>/dev/null; do sleep 15; done
export PICYC=./picyc.s
for f in 25 26; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-$f.txt out/s$f$m 10 200 --jobs $opt > /dev/null 2>&1; done; done
echo QUEUES DONE >> out/queueS.log
