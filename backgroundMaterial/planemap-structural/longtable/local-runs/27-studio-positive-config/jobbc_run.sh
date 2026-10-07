#!/bin/sh
for o in 25 26 27; do
  PICYC=./picyc.bc python3 run.py in-plantri-$o.txt out/bc$o 10 400 --jobbc
  PICYC=./picyc.bc python3 run.py in-plantri-$o.txt out/bc${o}m 10 400 --jobbc --mirror
done
PICYC=./picyc.bc python3 run.py jobbc-extra-graphs.txt out/bcx 2 1 --jobbc
PICYC=./picyc.bc python3 run.py jobbc-extra-graphs.txt out/bcxm 2 1 --jobbc --mirror
