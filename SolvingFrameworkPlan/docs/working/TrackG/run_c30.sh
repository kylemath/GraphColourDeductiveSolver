#!/bin/sh
# Track G: 25% sample of order-30 census (test set), runs after worker 1 finishes
cd "$(dirname "$0")"
until [ -f out/W1.done ]; do sleep 20; done
nice -n 10 python3 tg_collect.py ../Census29/out/frame-30.txt out/census30s4 --stride 4 --offset 0 > out/census30s4.log 2>&1
echo done > out/W4.done
