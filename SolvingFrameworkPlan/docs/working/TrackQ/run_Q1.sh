#!/bin/sh
# Track Q Part 1: exact minimum |E(G'-h)| on the three TrackP e=2 skeletons; CP-SAT (3 workers) || HiGHS (1 thread)
cd "$(dirname "$0")"
( for s in n1_7121_17_230_K_L_L n1_7121_103_1402_K_L n1_7221_43_1766_K_L; do
    nice -n 10 .venv/bin/python tq_arb.py out/${s}_data.json cpsat --tlim 3000 --workers 3 > out/min_cpsat_$s.log 2>&1
  done ) &
( for s in n1_7121_17_230_K_L_L n1_7121_103_1402_K_L n1_7221_43_1766_K_L; do
    nice -n 10 .venv/bin/python tq_arb.py out/${s}_data.json highs --tlim 2400 > out/min_highs_$s.log 2>&1
  done ) &
wait
