#!/bin/bash
# TrackO: IPR duals not covered by part 1 (which ran all 12 holes per graph); here first 4 holes per graph, 2 workers
cd "$(dirname "$0")/.."
for k in 0 1; do nice -n 10 src/to_eng4 -M 16000000 -k 4 < out/ipr_rest$k.txt > out/ipr_part2_$k.jsonl & done
wait
