#!/bin/zsh
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W
for a in "18 8689fdbce3a4e1246839" "19 f521dd185054dbcf9aaf"; do set -- ${=a}; echo "== h$1 $(date -u +%H:%M:%S)"; nice -n 10 python3 out/job_ST109/k109chk.py $1 $2 2>&1 | cut -c1-400; done
echo CHKDONE $(date -u +%H:%M:%S)
