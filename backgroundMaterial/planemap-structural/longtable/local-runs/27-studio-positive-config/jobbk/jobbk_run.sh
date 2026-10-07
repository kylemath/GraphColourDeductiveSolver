#!/bin/sh
while pgrep -f jobbj_search.py > /dev/null; do sleep 30; done
for o in 25 26 27; do
  PICYC=./picyc.bk python3 run.py in-plantri-$o.txt out/bk$o 12 400 --jobbk
  PICYC=./picyc.bk python3 run.py in-plantri-$o.txt out/bk${o}m 12 400 --jobbk --mirror
done
