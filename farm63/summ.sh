#!/bin/bash
# usage: summ.sh OUTDIR -> progress count plus KILL_D / KILL_C lines (window name, kc verdict line)
d=$1; echo "done $(ls $d/*.txt 2>/dev/null | wc -l)  notD $(cat $d/*.txt 2>/dev/null | grep -c 'D=false')  hostname $(hostname)"
for f in $d/*.txt; do [ -f "$f" ] || continue; if grep -q 'D=true' $f; then echo "KILL_D $(grep -m1 'D=true' $f | cut -c1-200)"; fi; if grep -q 'C-REDUCIBLE' $f; then echo "KILL_C $(grep -m1 'C-REDUCIBLE' $f | cut -c1-200)"; fi; done
