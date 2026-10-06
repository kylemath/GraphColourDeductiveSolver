#!/bin/bash
# start the K3 sweep when J12 has written its end time
cd "$(dirname "$0")"
until grep -q '^end' $HOME/studio-scratch/j12/out/times.txt 2>/dev/null; do sleep 60; done
nice -n 10 python3 k3scan.py 20 21 22 23 24 25 26 --workers 6 > k3-summary.jsonl 2> k3.err
echo "$(date '+%F %T') K3 DONE" >> k3-summary.log
