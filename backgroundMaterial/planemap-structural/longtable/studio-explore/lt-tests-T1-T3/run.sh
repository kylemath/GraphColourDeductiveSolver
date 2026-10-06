#!/bin/bash
# [exploratory] Long Table's Studio tests T1-T3 (message 1514 selection-sketches, commit 25243be), 600 CPU-s cap each, nice 10, 6 at a time.
S=$HOME/studio-scratch/main-wt2/backgroundMaterial/planemap-structural/longtable/explore-vhphi/pathways/sel_selection.py
O=$HOME/studio-scratch/lt-tests/out; mkdir -p "$O"
t() { local name=$1; shift; ( s=$(date +%s); ( ulimit -t 600; nice -n 10 python3 "$S" "$@" ) > "$O/$name.out" 2> "$O/$name.err"; echo "$name exit $? wall $(( $(date +%s)-s ))s" >> "$O/times.txt" ) & }
date '+start %F %T %Z' > "$O/times.txt"
t certmin certmin; t census census
t stack-6-3 stack 6 3; t stack-7-3 stack 7 3 one; t stack-8-3 stack 8 3 one; t stack-9-3 stack 9 3 one; wait
t stack-7-4 stack 7 4 one; t pair-pentakis pair pentakis; t pair-sixring28 pair sixring28 all; t pair-T4 pair T4 all; t pair-S6_3 pair S6_3; wait
date '+end %F %T %Z' >> "$O/times.txt"
