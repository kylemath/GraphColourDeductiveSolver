#!/bin/bash
# TrackO task 2: adversarial flip search (2 workers; engine calls run under nice 10)
cd "$(dirname "$0")/.."
nice -n 10 python3 src/to_search.py out/search_m5 --seeds out/seeds_all.txt --mindeg 5 --minutes 85 --batch 16 --seed 21 &
nice -n 10 python3 src/to_search.py out/search_m3 --seeds out/seeds_all.txt --mindeg 3 --nmax 60 --minutes 85 --batch 16 --seed 22 &
wait
