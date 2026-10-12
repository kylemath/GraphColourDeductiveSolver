#!/bin/bash
# TrackO task 1: plantri24, IPR fullerene duals C60-C100, fresh random spheres (nice 10; 4 workers)
cd "$(dirname "$0")/.."
F=../TrackF/graphs
E="nice -n 10 src/to_eng -M 16000000"
( $E < $F/plantri24.txt > out/plantri24.jsonl ) &
( $E < $F/ipr32_52.txt > out/ipr.jsonl ) &
( $E < out/fresh_m5_51_60.txt > out/fresh_m5_51_60.jsonl ) &
( for b in m5_20_30 m5_31_40 m5_41_50 m3_20_40 m3_41_60; do $E < out/fresh_$b.txt > out/fresh_$b.jsonl; done ) &
wait
