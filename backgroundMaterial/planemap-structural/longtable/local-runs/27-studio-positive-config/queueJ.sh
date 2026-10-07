#!/bin/bash
cd "$(dirname "$0")"
export PICYC=./picyc.h
nice -n 10 python3 run.py in-plantri-27.txt out/j27 12 200 --full --jobh > /dev/null 2>&1
nice -n 10 python3 run.py in-plantri-27.txt out/j27m 12 200 --full --jobh --mirror > /dev/null 2>&1
echo QUEUEJ DONE >> out/queueJ.log
