#!/bin/sh
cd "$(dirname "$0")/.."
for f in adv:jobbl/adversarial.txt c12:in-plantri-12-23.txt c24:in-plantri-24.txt c25:in-plantri-25.txt c26:in-plantri-26.txt c27:in-plantri-27.txt; do
  tag=${f%%:*}; inp=${f#*:}
  PICYC=./picyc.bl python3 run.py $inp out/bl$tag 2 400 --jobbl
  PICYC=./picyc.bl python3 run.py $inp out/bl${tag}m 2 400 --jobbl --mirror
done
