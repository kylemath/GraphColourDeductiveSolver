#!/bin/sh
# Track P Part A phase 5: continue from torus / Klein near-misses (all-DL 10-cycles with law penalty <= 3; still pure
# torus / Klein lineages), cycle-only law objective.
cd "$(dirname "$0")"
export TN_TLIM=2700 TN_CYCONLY=1
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7121 100000 2500 out/an_torus_near out/seeds_near_torus.txt > out/an_torus_near.log 2>&1 &
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7221 100000 2500 out/an_klein_near out/seeds_near_klein.txt > out/an_klein_near.log 2>&1 &
wait
