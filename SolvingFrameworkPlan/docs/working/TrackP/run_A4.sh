#!/bin/sh
# Track P Part A phase 4: cycle-only law objective from TrackF RP^2 all-DL cycle graphs (an RP^2 lineage independent of
# TrackH's rp2_s203 test bed used by TrackJ/TrackN).
cd "$(dirname "$0")"
export TN_TLIM=2400 TN_CYCONLY=1
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7611 100000 1500 out/an_rp2_cyc out/seeds_cyc_rp2.txt > out/an_rp2_cyc.log 2>&1 &
wait
