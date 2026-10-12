#!/bin/sh
# Track A phase 3: objective M (margin directly) on the census and constructed seeds. Waits for phase 2.
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
until grep -q ALLDONE out/search-phase2.log 2>/dev/null; do sleep 30; done
nice -n 10 python3 tracka_search.py out/seeds-census.json 400 2 out/search-census-M.jsonl M > out/search-census-M.log 2>&1
nice -n 10 python3 tracka_search.py out/seeds-constr.json 150 1 out/search-constr-M.jsonl M > out/search-constr-M.log 2>&1
echo ALLDONE >> out/search-constr-M.log
