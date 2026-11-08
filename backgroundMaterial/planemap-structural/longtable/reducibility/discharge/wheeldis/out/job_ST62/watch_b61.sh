#!/bin/bash
cd /Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/job_ST62
while true; do
  h=$(cat results/res_K5_*.tsv 2>/dev/null | awk -F'\t' '($5=="D" && $11 ~ /dfast18:D/) || ($5=="C" && $11 ~ /cfast:C-REDUCIBLE/)')
  [ -n "$h" ] && { echo "HIT"; echo "$h" | cut -c1-600; exit 0; }
  grep -q ALLDONE run.log && { echo ALLDONE; exit 0; }
  sleep 60
done
