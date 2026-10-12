#!/bin/sh
# extension of run.sh (7 Oct, after restart): 5 walks from the n = 48 best graphs, growing to n = 60, 4500 s wall each, 5 workers
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 POSW_POOL=5
nice -n 10 python3 posw_search.py posw/seeds2.json posw/search2.jsonl 4500 60 > posw/search2.log 2>&1
echo ALLDONE >> posw/search2.log
