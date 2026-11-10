#!/bin/zsh
# HCK5P22 after HCK5P21's Lean (ALLDONE); alongside HDST111
J=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q ALLDONE $J/job_HCK5P21/lean/status.txt 2>/dev/null; do sleep 120; done
echo "start HCK5P22 $(date -u +%H:%M)"; zsh $J/job_HCK5P22/drive.sh > $J/job_HCK5P22/drive.log 2>&1; tail -4 $J/job_HCK5P22/lean/status.txt; echo QDONE
