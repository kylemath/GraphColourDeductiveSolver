#!/bin/sh
cd "$(dirname "$0")"
OUTDIR=out/parts2 T=p2b_ P=4 ./run_all.sh jobs_pass2b.txt
for n in 22 23 24 25 26 27 28; do nice -n 10 python3 tm_kempe1879.py out/kempe1879.jsonl rot:../Census29/out/frame-$n.txt; done
nice -n 10 python3 tm_kempe1879.py out/kempe1879.jsonl rot:../Census29/out/frame-30.txt --names 'p30.r10#1252'
echo chain done >> out/logs/done.txt
