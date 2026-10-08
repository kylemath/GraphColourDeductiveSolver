#!/bin/sh
# Track N: control searches f=1 (R-cycle + law, no Lemma E), adaptive walk length (extends while improving if best >= 15)
cd "$(dirname "$0")"
export TN_TLIM=${TN_TLIM:-3600}
TN_MOVES=2:2:3:1:2:3 nice -n 10 python3 tn_search.py 1 1102 100000 1000 out/anneal_f1_sphere out/seeds_run67.txt > out/anneal_f1_sphere.log 2>&1 &
TN_MOVES=2:2:3:1:2:3 nice -n 10 python3 tn_search.py 1 1202 100000 1000 out/anneal_f1_rp2 ../TrackJ/out/rp2_graphs.txt > out/anneal_f1_rp2.log 2>&1 &
TN_MOVES=2:2:3:1:2:3 nice -n 10 python3 tn_search.py 1 1302 100000 1000 out/anneal_f1_tk ../TrackJ/out/torusklein_graphs.txt > out/anneal_f1_tk.log 2>&1 &
wait
