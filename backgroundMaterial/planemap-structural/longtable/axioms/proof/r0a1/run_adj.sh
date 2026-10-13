#!/bin/sh
# closed walks in D for planar graphs with a Ham cycle through ADJACENT v-edges (C30#0 type; no Ham arc needed)
for a in "adj 16 10" "adj 18 10" "adj 20 10" "adj 16 20" "adj 18 20" "adj 20 20" "adj 22 20" "adj 22 10" "adj 24 20"; do
  nice -n 10 python3 r0sat.py $a t=400
done
