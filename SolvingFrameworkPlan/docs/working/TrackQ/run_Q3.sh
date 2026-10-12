#!/bin/sh
# Track Q Part 1b (LP-only pass): mcf LP lower bound on 4 law-cycle graphs sampled evenly from each lineage file (out/batch_sample.txt); MILP only if LP excess <= 0
cd "$(dirname "$0")"
P=../TrackP/out
F="out/batch_sample.txt"
export TQ_LPONLY=1
for s in 0 1 2; do nice -n 10 .venv/bin/python tq_batch.py out/batch_lp_s$s.jsonl $s 3 600 $F > out/batch_lp_s$s.log 2>&1 & done
wait
