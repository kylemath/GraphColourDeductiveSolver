#!/bin/sh
# Track P Part A phase 7: direct N1 attack from the excess-2 law cycles (torus x2, Klein, sphere lineages):
# f = 3 cycle-only objective P = sum max(0,N-9) + sum dev + law fails over the best all-DL cycle (dev = Lemma E deviation),
# unrestricted graph moves (partitions may change).  An example = law R-cycle with (2,3,3) at every state = N1 counterexample.
cd "$(dirname "$0")"
export TN_TLIM=1500 TN_CYCONLY=1
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 3 7811 100000 3000 out/an_f3_exc2a out/seeds_exc2.txt > out/an_f3_exc2a.log 2>&1 &
TN_MOVES=3:1:3:0:0:5 nice -n 10 python3 tn_search.py 3 7812 100000 3000 out/an_f3_exc2b out/seeds_exc2.txt > out/an_f3_exc2b.log 2>&1 &
wait
