#!/bin/sh
cd "$(dirname "$0")/.."
while pgrep -f jobbl_run.sh > /dev/null; do sleep 20; done
for f in ipr:in-ipr.txt adv:jobbl/adversarial.txt c12:in-plantri-12-23.txt c24:in-plantri-24.txt c25:in-plantri-25.txt c26:in-plantri-26.txt c27:in-plantri-27.txt; do
  tag=${f%%:*}; inp=${f#*:}
  PICYC=./picyc.bo python3 run.py $inp out/bo$tag 2 200 --jobbo
  PICYC=./picyc.bo python3 run.py $inp out/bo${tag}m 2 200 --jobbo --mirror
done
