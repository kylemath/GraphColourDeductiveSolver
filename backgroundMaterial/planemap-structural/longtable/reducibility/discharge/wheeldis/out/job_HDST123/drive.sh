#!/bin/zsh
# HDST123: hD for nl2208_r13 (ST-123), on the substitute slot after the ST-119 queue (QDONE)
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q QDONE $O/job_ST119/queue_lean.log 2>/dev/null; do sleep 120; done
cd $O/job_HDST123/lean && ./run.sh HDST123 && ./run.sh HDST123V00 && ./run.sh HDST123All; echo ALLDONE >> status.txt
