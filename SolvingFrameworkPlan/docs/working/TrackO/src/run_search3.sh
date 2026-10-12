#!/bin/bash
# TrackO task 2, frame-class wave: flips restricted to the frame class, seeded from census R>=5 graphs (1 worker)
cd "$(dirname "$0")/.."
nice -n 10 python3 src/to_search.py out/search3_frame --seeds out/seeds_census_R5.txt --mindeg 5 --frame --minutes 85 --batch 48 --seed 41 --restart 300 &
wait
