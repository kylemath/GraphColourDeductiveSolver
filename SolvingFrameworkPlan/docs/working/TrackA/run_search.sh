#!/bin/sh
# Track A search runs (sequential, each Pool(4), nice 10, single-threaded)
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
nice -n 10 python3 tracka_search.py out/seeds-census.json 400 2 out/search-census.jsonl R,W > out/search-census.log 2>&1
nice -n 10 python3 tracka_search.py out/seeds-constr.json 150 1 out/search-constr.jsonl R,W > out/search-constr.log 2>&1
echo ALLDONE >> out/search-constr.log
