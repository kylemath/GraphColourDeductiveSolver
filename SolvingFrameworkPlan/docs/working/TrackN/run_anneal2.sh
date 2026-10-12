#!/bin/sh
# Track N annealing, phase 2: law-respecting R-cycles (f = 1) from RP^2 and torus/Klein seeds (diverse origins for tn_forest)
cd "$(dirname "$0")"
export TN_TLIM=3600
TN_MOVES=2:2:3:1:1:3 nice -n 10 python3 tn_search.py 1 1201 100000 1500 out/anneal_f1_rp2 ../TrackJ/out/rp2_graphs.txt > out/anneal_f1_rp2.log 2>&1 &
TN_MOVES=2:2:3:1:1:3 nice -n 10 python3 tn_search.py 1 1301 100000 1500 out/anneal_f1_tk ../TrackJ/out/torusklein_graphs.txt > out/anneal_f1_tk.log 2>&1 &
wait
