#!/bin/sh
# Track Q Part 1b: exact min excess on every available law R-cycle (TrackP lineages), 4 shards x 1 HiGHS thread (mcf LP bound, then MILP if needed)
cd "$(dirname "$0")"
P=../TrackP/out
F="$P/seeds_exc2.txt $P/ex_sphere_w15.jsonl $P/ex_sphere_batch1.jsonl $P/ex_sphere_3.jsonl $P/ex_torus_s1.jsonl $P/ex_torus_lineages.jsonl $P/ex_klein_lineages.jsonl $P/ex_klein_w34.jsonl $P/an_sphere_cyc.jsonl $P/an_torus_near.jsonl $P/an_klein_near.jsonl"
for s in 0 1 2 3; do nice -n 10 .venv/bin/python tq_batch.py out/batch_s$s.jsonl $s 4 600 $F > out/batch_s$s.log 2>&1 & done
wait
