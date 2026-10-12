#!/bin/sh
cd "$(dirname "$0")"
export TJ_TLIM=2400
nice -n 10 python3 tj_sphsearch.py 801 100000 300 out/sphflip.jsonl out/sphere_flip_seeds.txt > out/sphflip.log 2>&1 &
TJ_CHI=1 nice -n 10 python3 tj_sphsearch.py 901 100000 300 out/rp2flip.jsonl out/rp2_graphs.txt > out/rp2flip.log 2>&1 &
nice -n 10 python3 tj_search.py h 611 100000 8000 out/search_h2 out/seeds_tex.txt out/seeds_cex.txt out/seeds_sphere.txt > out/search_h2.log 2>&1 &
wait
