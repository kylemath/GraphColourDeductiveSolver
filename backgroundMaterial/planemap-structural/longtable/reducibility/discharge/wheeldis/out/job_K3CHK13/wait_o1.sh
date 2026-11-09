#!/bin/bash
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W
while pgrep -f maclane/st70b.sh > /dev/null; do sleep 30; done
nice -n 10 python3 out/job_K3CHK13/k13chk.py O1 2>&1 | tail -12 | cut -c1-300
