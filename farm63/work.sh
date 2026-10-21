#!/bin/bash
# usage: bash farm63/work.sh CHUNKFILE   (run from repo root). Compiles kc, runs every window with kc -C -s 60 -t 600 on 4 cores.
set -u
C=$1; B=$(basename $C .txt); mkdir -p /tmp/w/$B; g++ -O2 -o /tmp/w/kcc farm63/kc.cpp || exit 1
run1() { N=$(echo "$1" | cut -d' ' -f1); echo "$1" | timeout 900 /tmp/w/kcc -C -s 60 -t 600 > /tmp/w/$2/$N.tmp 2>&1 && mv /tmp/w/$2/$N.tmp /tmp/w/$2/$N.txt; }
export -f run1
grep -v '^$' $C | xargs -d '\n' -P4 -I{} bash -c 'run1 "$1" '$B {} _ >/dev/null 2>&1
echo DONE > /tmp/w/$B.done
