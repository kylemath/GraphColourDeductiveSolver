#!/bin/sh
# Track P Part A phase 6: genus 2.  Seeds = best holes (law-window penalty 4-9) of the genus-2 flip-search graphs
# (lpc_cycsearch found DL pi-runs up to 18 but no all-DL cycle).  Window+cycle law objective, no stacking.
cd "$(dirname "$0")"
export TN_TLIM=2400
TN_MOVES=2:2:4:0:0:3 nice -n 10 python3 tn_search.py 1 7711 100000 2000 out/an_g2 out/prec_g2_seeds.txt > out/an_g2.log 2>&1 &
wait
