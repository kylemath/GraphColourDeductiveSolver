#!/bin/sh
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
nice -n 10 python3 posw_search.py posw/seeds.json posw/search.jsonl 3000 48 > posw/search.log 2>&1
echo ALLDONE >> posw/search.log
