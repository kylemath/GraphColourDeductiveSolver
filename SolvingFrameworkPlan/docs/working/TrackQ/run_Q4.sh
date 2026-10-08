#!/bin/sh
# Track Q: direct N1 attack from the e = 1 law cycle (TrackP run_A7 objective f = 3, cycle-only, unrestricted moves:
# partitions may change).  An 'example' = law R-cycle with Lemma E (2,3,3) at every state = e = 0 = N1 counterexample.
cd "$(dirname "$0")"
export TN_TLIM=1500 TN_CYCONLY=1
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 3 9101 100000 3000 out/an_f3_e1 out/e1_examples.txt > out/an_f3_e1.log 2>&1
