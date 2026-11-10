#!/bin/bash
# u smokes, serialised after the t smokes
M=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane
until grep -q 'T-SMOKES-END' $M/setup_k5t/smokes.log 2>/dev/null; do sleep 60; done
echo "t smokes done $(date -u +%H:%MZ); start u"; bash $M/setup_k5u/smokes.sh; echo "U-SMOKES-END $(date -u +%H:%MZ)"
