#!/bin/sh
cd "$(dirname "$0")"
S="out/seeds_general.txt out/seeds_surface.txt out/seeds_sphere.txt"
export TJ_TLIM=2700
nice -n 10 python3 tj_search.py b 201 100000 6000 out/search_b1 $S > out/search_b1.log 2>&1 &
nice -n 10 python3 tj_search.py b 202 100000 6000 out/search_b2 out/seeds_sphere.txt out/seeds_surface.txt > out/search_b2.log 2>&1 &
nice -n 10 python3 tj_search.py c 301 100000 6000 out/search_c $S > out/search_c.log 2>&1 &
nice -n 10 python3 tj_search.py d 401 100000 6000 out/search_d $S > out/search_d.log 2>&1 &
wait
