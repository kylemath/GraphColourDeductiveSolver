#!/bin/sh
# Track F slot 1: lock-parity sweep + all-DL detection on small graphs (exhaustive)
cd "$(dirname "$0")/.."
for f in frame22_28 plantri24; do
  nice -n 10 ./src/f66_w1_new graphs/$f.txt --lockparity --dump 10 --dumpfile out/sweep/$f.runs.jsonl > out/sweep/$f.holes.jsonl 2> out/sweep/$f.err
done
echo done > out/sweep/DONE
