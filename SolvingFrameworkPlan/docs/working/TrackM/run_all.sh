#!/bin/sh
# Track M: run the job list with at most $P workers, nice 10. Each job appends to its own out file
# (jobs sharing a file use a per-job temp file, concatenated at the end).
cd "$(dirname "$0")"; P=${P:-3}; J=${1:-jobs_main.txt}
OUTDIR=${OUTDIR:-out/parts}; export OUTDIR
mkdir -p $OUTDIR out/logs
i=0
while read -r line; do i=$((i+1)); echo "${T:-}$i $line"; done < "$J" | \
  xargs -P "$P" -L 1 sh -c 'n=$0; out=$1; shift; nice -n 10 python3 tm_run.py ${OUTDIR:-out/parts}/$n.$(basename $out) "$@" 2> out/logs/$n.log; echo "job $n done" >> out/logs/done.txt'
