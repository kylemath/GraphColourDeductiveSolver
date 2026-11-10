#!/bin/bash
# u smokes, serialised after the u smokes
M=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane
until grep -q 'U-SMOKES-END' $M/setup_k5u/smokes.log 2>/dev/null; do sleep 60; done
echo "u smokes done $(date -u +%H:%MZ); start v"; bash $M/setup_k5v/smokes.sh; echo "V-SMOKES-END $(date -u +%H:%MZ)"
