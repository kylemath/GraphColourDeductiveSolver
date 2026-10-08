#!/bin/sh
cd "$(dirname "$0")"
S="out/seeds_cex.txt out/seeds_general.txt out/seeds_surface.txt out/seeds_sphere.txt"
export TJ_TLIM=2400
nice -n 10 python3 tj_search.py t 511 100000 6000 out/search_t $S > out/search_t.log 2>&1 &
nice -n 10 python3 tj_search.py d 711 100000 6000 out/search_d $S > out/search_d.log 2>&1 &
wait
