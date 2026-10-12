#!/bin/sh
cd "$(dirname "$0")/.."
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
nice -n 10 python3 anatomy.py anat/anat-census27-28.jsonl out/frame-27.txt out/frame28-cfree-list.txt > anat/run.log 2>&1
nice -n 10 python3 anatomy.py anat/anat-wbest.jsonl --faces anat/wbest-graphs.json >> anat/run.log 2>&1
echo ALLDONE >> anat/run.log
