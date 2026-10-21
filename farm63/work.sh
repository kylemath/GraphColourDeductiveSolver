#!/bin/bash
# usage: bash farm63/work.sh OUTDIR CHUNKFILE...   (run from repo root)
# Compiles kc, runs every window line with kc -C -s 60 -t 600, 4 at a time. One output file per window in OUTDIR.
set -u
O=$1; shift; mkdir -p $O; g++ -O2 -o $O/kcc farm63/kc.cpp || exit 1
run1() { N=${1%% *}; [ -s $O/$N.txt ] && return; echo "$1" | timeout 900 $O/kcc -C -s 60 -t 600 > $O/$N.tmp 2>&1; [ -s $O/$N.tmp ] && mv $O/$N.tmp $O/$N.txt; }
export -f run1; export O
cat "$@" | grep -v '^$' | xargs -d '\n' -P4 -I{} bash -c 'run1 "$1"' _ {} >/dev/null 2>&1
echo DONE > $O/ALL.done
