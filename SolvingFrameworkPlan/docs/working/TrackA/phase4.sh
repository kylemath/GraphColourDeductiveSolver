#!/bin/sh
# Track A phase 4: long M walks (1000 steps) from the phase-2 seeds (n = 32, 36, IPR 32). Waits for phase 3.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
until grep -q ALLDONE out/search-constr-M.log 2>/dev/null; do sleep 30; done
nice -n 10 python3 tracka_search.py out/seeds-phase2.json 1000 1 out/search-phase4-M.jsonl M > out/search-phase4-M.log 2>&1
echo ALLDONE >> out/search-phase4-M.log
