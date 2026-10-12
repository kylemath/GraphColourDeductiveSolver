#!/bin/sh
# Track N: window objective with Lemma E from sphere seeds (long R-runs): f=3 (law + E) and f=2 (E only)
cd "$(dirname "$0")"
export TN_TLIM=${TN_TLIM:-2700}
TN_MOVES=3:3:1:1:2:4 nice -n 10 python3 tn_search.py 3 3201 100000 1000 out/anneal_f3_sphere out/seeds_run67.txt > out/anneal_f3_sphere.log 2>&1 &
TN_MOVES=3:3:1:1:2:4 nice -n 10 python3 tn_search.py 2 2201 100000 1000 out/anneal_f2_sphere out/seeds_run67.txt > out/anneal_f2_sphere.log 2>&1 &
wait
