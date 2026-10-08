#!/bin/bash
# TrackO task 2, second wave: searches seeded from the verified R=7 graph (2 workers)
cd "$(dirname "$0")/.."
nice -n 10 python3 src/to_search.py out/search2_m5 --seeds out/hit_R7.txt --mindeg 5 --minutes 80 --batch 16 --seed 31 --restart 400 &
nice -n 10 python3 src/to_search.py out/search2_m3 --seeds out/hit_R7.txt --mindeg 3 --nmax 36 --minutes 80 --batch 16 --seed 32 --restart 400 &
wait
