#!/bin/zsh
# ST-109: run HCK5P18 then HCK5P19 after HCK5P17 ALLDONE (Lean one at a time)
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W
until grep -q ALLDONE out/job_HCK5P17/lean/status.txt 2>/dev/null; do sleep 60; done
for n in 18 19; do echo "start HCK5P$n $(date -u +%H:%M)"; zsh out/job_HCK5P$n/drive.sh > out/job_HCK5P$n/drive.log 2>&1; tail -4 out/job_HCK5P$n/lean/status.txt; done
echo QDONE $(date -u +%H:%M)
