#!/bin/sh
# R0* (closed walk anywhere in D of a planar graph that has the Ham arc M0->M1) and R0 for comparison
for a in "star 20 10" "star 22 10" "star 16 20" "star 18 20" "star 20 5" "star 24 5" "star 24 10" "star 20 20" "star 26 10"; do
  nice -n 10 python3 r0sat.py $a t=550
done
