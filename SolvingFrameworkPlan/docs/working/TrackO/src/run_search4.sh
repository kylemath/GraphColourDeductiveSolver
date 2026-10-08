#!/bin/bash
# TrackO task 2, small-order wave: min-degree-5 flips at n=24 from plantri24 graphs with R=5 (1 worker)
cd "$(dirname "$0")/.."
nice -n 10 python3 src/to_search.py out/search4_p24 --seeds out/seeds_plantri24_R5.txt --mindeg 5 --minutes 35 --batch 16 --seed 51 --restart 200
