#!/bin/sh
# Round 1, replacement worker: FL_n12 had no legal flip (every flip drops a belt vertex to degree 4 or breaks max degree), so it stopped
# after its seed evaluation; SL_rings8-9-9 (Math's slipped stack, top priority family) takes its core for the rest of the round.
cd "$(dirname "$0")"; nice -n 10 python3 kc_search_local.py build/core/SL_rings8-9-9.json 17 8 4 1080 run1 9 SL_rings8-9-9 > run1/SL_rings8-9-9.out 2>&1
