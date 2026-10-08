#!/bin/sh
# Track P Part A phase 3: cycle-only law objective from sphere all-DL cycle graphs (TrackJ sphere_cycle_graphs: Census29 + C30#0).
cd "$(dirname "$0")"
export TN_TLIM=3000 TN_CYCONLY=1
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7511 100000 1500 out/an_sphere_cyc out/seeds_cyc_sphere.txt > out/an_sphere_cyc.log 2>&1 &
wait
