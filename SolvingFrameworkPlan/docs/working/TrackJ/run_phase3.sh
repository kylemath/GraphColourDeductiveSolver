#!/bin/sh
cd "$(dirname "$0")"
export TJ_TLIM=1500
nice -n 10 python3 tj_search.py h 621 100000 8000 out/search_h3a out/seeds_h3near.txt > out/search_h3a.log 2>&1 &
TJ_GROW=4 nice -n 10 python3 tj_search.py h 622 100000 8000 out/search_h3b out/seeds_h3near.txt > out/search_h3b.log 2>&1 &
TJ_GROW=4 nice -n 10 python3 tj_search.py d 623 100000 8000 out/search_d3 out/seeds_h3near.txt > out/search_d3.log 2>&1 &
wait
