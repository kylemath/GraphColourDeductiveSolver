#!/bin/bash
# TrackO task 1: exhaustive R on Census29 frame 30-32 (nice 10; frame-32 split in 4 shards by line number)
cd "$(dirname "$0")/.."
C=../Census29/out
nice -n 10 src/to_eng < $C/frame-31.txt > out/frame-31.jsonl &
for k in 0 1 2 3; do
  awk -v k=$k 'NR%4==k' $C/frame-32.txt | nice -n 10 src/to_eng > out/frame-32.s$k.jsonl &
done
wait
