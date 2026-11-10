#!/bin/bash
# t smokes, serialised after the s smokes (load ~37 on 16 cores at 11:49Z)
M=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out/maclane
until grep -q 'SMOKE-FAM s:' $M/setup_k5s/smoke_fam_s.out 2>/dev/null; do sleep 60; done
echo "s smokes done $(date -u +%H:%MZ); start t"; bash $M/setup_k5t/smokes.sh; echo "T-SMOKES-END $(date -u +%H:%MZ)"
