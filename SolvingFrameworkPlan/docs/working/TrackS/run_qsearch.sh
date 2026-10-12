#!/bin/sh
# Track S: adversarial sphere flip search for low-level Q-cycles (1 worker, nice 10, 45 min).
cd "$(dirname "$0")"
TS_TLIM=2700 nice -n 10 python3 ts_qsearch.py 11 400 150 out/qsearch.jsonl ../TrackF/graphs/fall_20_46.txt,../TrackJ/out/sphere_cycle_graphs.txt,../TrackF/graphs/fall_24.txt > out/qsearch.log 2>&1
