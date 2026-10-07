#!/bin/sh
cd "$(dirname "$0")/.."
sleep 60; while pgrep -f "jobbj_c.py|jobbj_c_run.sh" > /dev/null; do sleep 30; done
PICYC=./picyc.bt python3 run.py jobbt/hits61.txt out/bthits 8 1 --jobbt
PICYC=./picyc.bt python3 run.py jobbt/hits61.txt out/bthitsm 8 1 --jobbt --mirror
for o in 25 26 27; do
  PICYC=./picyc.bt python3 run.py in-plantri-$o.txt out/bt$o 8 400 --jobbt
  PICYC=./picyc.bt python3 run.py in-plantri-$o.txt out/bt${o}m 8 400 --jobbt --mirror
done
