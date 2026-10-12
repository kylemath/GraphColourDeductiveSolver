#!/bin/sh
cd "$(dirname "$0")/.."
while pgrep -f jobbo_run.sh > /dev/null; do sleep 20; done
for f in ipr:in-ipr.txt adv:jobbl/adversarial.txt c12:in-plantri-12-23.txt c24:in-plantri-24.txt c25:in-plantri-25.txt c26:in-plantri-26.txt c27:in-plantri-27.txt; do
  tag=${f%%:*}; inp=${f#*:}
  PICYC=./picyc.bp python3 run.py $inp out/bp$tag 2 200 --jobbp
  PICYC=./picyc.bp python3 run.py $inp out/bp${tag}m 2 200 --jobbp --mirror
done
