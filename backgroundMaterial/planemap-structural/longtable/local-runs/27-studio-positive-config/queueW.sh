#!/bin/bash
cd "$(dirname "$0")"
export PICYC=./picyc.w
for f in 25 26 27; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; nice -n 10 python3 run.py in-plantri-$f.txt out/w$f$m 14 400 --jobx $opt > /dev/null 2>&1; done; done
echo W DONE >> out/queueW.log
for f in 25 26 27; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; rm -rf out/sx$f$m.shards; nice -n 10 python3 run.py in-plantri-$f.txt out/sx$f$m 14 400 --jobs $opt > /dev/null 2>&1; done; done
echo SX DONE >> out/queueW.log
for f in 25 26 27; do for m in "" m; do opt=""; [ "$m" = m ] && opt=--mirror; rm -rf out/z$f$m.shards out/z$f$m.jsonl; nice -n 10 python3 run.py in-plantri-$f.txt out/z$f$m 14 400 --jobz $opt > /dev/null 2>&1; done; done
echo Z DONE >> out/queueW.log
