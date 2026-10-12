#!/bin/sh
# Track N annealing, phase 1 (<= 2 workers here; others run tn_forest/tn_flow)
cd "$(dirname "$0")"
export TN_TLIM=4500
TN_MINDEG=2 TN_MOVES=2:1:2:1:1:4 nice -n 10 python3 tn_search.py 3 3101 100000 1500 out/anneal_f3_reduced out/seeds_reduced.txt > out/anneal_f3_reduced.log 2>&1 &
TN_MOVES=2:2:3:1:1:3 nice -n 10 python3 tn_search.py 1 1101 100000 1500 out/anneal_f1_sphere out/seeds_run67.txt > out/anneal_f1_sphere.log 2>&1 &
wait
