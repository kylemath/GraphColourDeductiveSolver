#!/bin/bash
cd "$(dirname "$0")"
while ! grep -q "QUEUE2 DONE" out/queue2.log 2>/dev/null; do sleep 30; done
for n in 27 28; do
  nice -n 10 python3 run.py in-cfree-$n.txt out/cf$n 12 1 --full > out/cf$n.stdout 2>&1
  nice -n 10 python3 run.py in-cfree-$n.txt out/cf${n}m 12 1 --full --mirror > out/cf${n}m.stdout 2>&1
done
echo QUEUE3 DONE >> out/queue3.log
