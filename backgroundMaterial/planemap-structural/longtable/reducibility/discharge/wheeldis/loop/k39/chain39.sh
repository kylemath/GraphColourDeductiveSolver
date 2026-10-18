#!/bin/bash
# start round 39 once round 38's greedy loop (pid given) exits
cd "$(dirname "$0")"
while kill -0 "$1" 2>/dev/null; do sleep 10; done
NW=1 python3 drive39.py p5.txt 17 2400 > drive39.log 2>&1
echo done > R39.DONE
