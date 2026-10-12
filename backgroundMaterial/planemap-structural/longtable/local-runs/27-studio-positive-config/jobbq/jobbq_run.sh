#!/bin/sh
cd "$(dirname "$0")/.."


for f in adv:jobbl/adversarial.txt c25:in-plantri-25.txt c26:in-plantri-26.txt c27:in-plantri-27.txt; do
  tag=${f%%:*}; inp=${f#*:}
  PICYC=./picyc.bq python3 run.py $inp out/bq$tag 8 200 --jobbq
  PICYC=./picyc.bq python3 run.py $inp out/bq${tag}m 8 200 --jobbq --mirror
done
