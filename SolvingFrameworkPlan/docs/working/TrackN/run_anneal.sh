#!/bin/sh
# Track N annealing (4 workers, nice 10).  W1: Q-e objective f=3 from the ILP-reduced TrackJ examples (dev 3/state);
# W2: control f=1 (law, no Lemma E) from sphere seeds with long R-runs; W3/W4: f=1 from RP^2 / torus+Klein seeds
# (diverse origins for law-respecting R-cycles, later reduced by tn_forest.py).
cd "$(dirname "$0")"
export TN_TLIM=${TN_TLIM:-3600}
TN_MINDEG=2 TN_MOVES=2:1:2:1:2:4 nice -n 10 python3 tn_search.py 3 3101 100000 1000 out/anneal_f3_reduced out/seeds_reduced.txt > out/anneal_f3_reduced.log 2>&1 &
TN_MOVES=2:2:3:1:2:3 nice -n 10 python3 tn_search.py 1 1101 100000 1000 out/anneal_f1_sphere out/seeds_run67.txt > out/anneal_f1_sphere.log 2>&1 &
TN_MOVES=2:2:3:1:2:3 nice -n 10 python3 tn_search.py 1 1201 100000 1000 out/anneal_f1_rp2 ../TrackJ/out/rp2_graphs.txt > out/anneal_f1_rp2.log 2>&1 &
TN_MOVES=2:2:3:1:2:3 nice -n 10 python3 tn_search.py 1 1301 100000 1000 out/anneal_f1_tk ../TrackJ/out/torusklein_graphs.txt > out/anneal_f1_tk.log 2>&1 &
wait
