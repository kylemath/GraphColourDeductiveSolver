#!/bin/zsh
# HCK5P20 then HCK5P21 (CK + V00 + VAll), after HCK5P19 GLUEDONE; runs alongside HDST111 (whose own order is unchanged)
J=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q GLUEDONE $J/job_HCK5P19/lean/status.txt 2>/dev/null; do sleep 120; done
for n in 20 21; do echo "start HCK5P$n $(date -u +%H:%M)"; zsh $J/job_HCK5P$n/drive.sh > $J/job_HCK5P$n/drive.log 2>&1; tail -4 $J/job_HCK5P$n/lean/status.txt; done
echo QDONE $(date -u +%H:%M)
