#!/bin/sh
# Track P Part A phase 2: cycle-only law objective (keep the seed's all-DL pi-cycle, drive P_law -> 0), no vertex stacking.
cd "$(dirname "$0")"
export TN_TLIM=3000 TN_CYCONLY=1
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7111 100000 1500 out/an_torus_cyc out/seeds_cyc_torus.txt > out/an_torus_cyc.log 2>&1 &
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7211 100000 1500 out/an_klein_cyc out/seeds_cyc_klein.txt > out/an_klein_cyc.log 2>&1 &
wait
