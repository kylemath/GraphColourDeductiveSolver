#!/bin/bash
# TrackO task 1 (rerun with final engine to_eng3 = to_eng.c with -D dump cap and runsNR): census 22-32, BV, fresh spheres
cd "$(dirname "$0")/.."
E="nice -n 10 src/to_eng3 -M 16000000"
C=../Census29/out
( $E < out/fresh_m5_51_60.txt > out/fresh_m5_51_60.jsonl ) &
( for b in m5_41_50 m5_20_30 m5_31_40 m3_20_40 m3_41_60; do $E < out/fresh_$b.txt > out/fresh_$b.jsonl; done ) &
( for k in 22 23 24 25 26 27 28 29 30 31 32; do $E < $C/frame-$k.txt > out/frame-$k.jsonl; done; rm -f out/frame-32.s?.jsonl; $E < out/bv.txt > out/bv.jsonl ) &
wait
