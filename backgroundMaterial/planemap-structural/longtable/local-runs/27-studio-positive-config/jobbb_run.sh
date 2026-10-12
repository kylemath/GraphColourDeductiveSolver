#!/bin/sh
for o in 25 26 27; do
  PICYC=./picyc.bb python3 run.py in-plantri-$o.txt out/bb$o 10 400 --jobbb
  PICYC=./picyc.bb python3 run.py in-plantri-$o.txt out/bb${o}m 10 400 --jobbb --mirror
done
