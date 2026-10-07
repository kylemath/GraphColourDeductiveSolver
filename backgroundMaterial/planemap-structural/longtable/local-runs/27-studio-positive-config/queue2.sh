#!/bin/bash
# wait for the order-26 mirror run, then IPR (both chiralities) and the big sample (both chiralities)
cd "$(dirname "$0")"
while [ ! -f out/p26m.jsonl ]; do sleep 30; done
nice -n 10 python3 run.py in-ipr.txt out/ipr 12 10 > out/ipr.stdout 2>&1
nice -n 10 python3 run.py in-ipr.txt out/iprm 12 10 --mirror > out/iprm.stdout 2>&1
nice -n 10 python3 run.py in-bigsample.txt out/big 9 1 > out/big.stdout 2>&1
nice -n 10 python3 run.py in-bigsample.txt out/bigm 9 1 --mirror > out/bigm.stdout 2>&1
echo QUEUE2 DONE >> out/queue2.log
