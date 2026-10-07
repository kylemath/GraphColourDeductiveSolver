#!/bin/sh
cd "$(dirname "$0")/.."
for f in c12:in-plantri-12-23.txt c24:in-plantri-24.txt c25:in-plantri-25.txt c26:in-plantri-26.txt c27:in-plantri-27.txt adv:jobbl/adversarial.txt; do
  tag=${f%%:*}; inp=${f#*:}
  PICYC=./picyc.bu python3 run.py $inp out/bu$tag 2 400 --jobbu
  PICYC=./picyc.bu python3 run.py $inp out/bu${tag}m 2 400 --jobbu --mirror
done
