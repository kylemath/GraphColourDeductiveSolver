#!/bin/bash
# Track U second wave (one worker slot): random census, then many short mode-A anneals
cd "$(dirname "$0")"; O=out
for nn in 22 26 30 34; do nice -n 10 ./tu_eng2 anneal 77$nn $nn 200 R 1 > $O/rand_n$nn.jsonl; done
for s in 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20; do for nn in 24 26 28 30; do
  nice -n 10 ./tu_eng2 anneal 9$s$nn $nn 30 A 1 > $O/shortA_n${nn}_s$s.jsonl; done; done
