#!/bin/bash
# J3: audit's WP20 P1 replay, route A, run from a detached worktree of origin/main.
cd "$HOME/studio-scratch/main-wt" || exit 1
LT=backgroundMaterial/planemap-structural/longtable
OUT="$HOME/studio-scratch/p1audit/out"
mkdir -p "$OUT"
date '+start: %F %T %Z' > "$OUT/times.txt"
( ulimit -t 7200; LONGTABLE_DIR="$LT" nice -n 10 python3 $LT/audit/wp20-replay/compare_p1.py \
    "$HOME/studio-scratch/p1audit/P1-m5-25.json" $LT/wp20/input-m5-25.txt --workers 2 --out "$OUT" ) 2>&1 | tee "$OUT/run.log"
echo "exit: ${PIPESTATUS[0]}" >> "$OUT/times.txt"
date '+end: %F %T %Z' >> "$OUT/times.txt"
