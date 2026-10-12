#!/bin/sh
# Track P Part A phase 1 (4 workers, nice 10): law-respecting R-cycles from torus / Klein seeds (TrackF all-DL cycle graphs),
# plus a genus-2 all-DL cycle search (TrackF lpc_cycsearch, read-only).
cd "$(dirname "$0")"
export TN_TLIM=3300 TJ_TLIM=3300
TN_MOVES=2:2:3:1:1:3 nice -n 10 python3 tn_search.py 1 7101 100000 1500 out/an_torus_tn out/seeds_cyc_torus.txt > out/an_torus_tn.log 2>&1 &
TN_MOVES=2:2:3:1:1:3 nice -n 10 python3 tn_search.py 1 7201 100000 1500 out/an_klein_tn out/seeds_cyc_klein.txt > out/an_klein_tn.log 2>&1 &
nice -n 10 python3 tj_search.py b 7301 100000 6000 out/an_tk_tjb out/seeds_cyc_torus.txt out/seeds_cyc_klein.txt > out/an_tk_tjb.log 2>&1 &
LPC_OBJ=count nice -n 10 python3 ../TrackF/src/lpc_cycsearch.py genus2 60 2000 24 34 7401 out/g2cyc > out/g2cyc.log 2>&1 &
wait
