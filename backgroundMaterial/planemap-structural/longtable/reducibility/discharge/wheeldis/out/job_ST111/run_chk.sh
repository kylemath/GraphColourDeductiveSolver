#!/bin/zsh
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis; cd $W
for a in "S1 fix_63c8a193fe" "S2 fix_404d45e819"; do set -- ${=a}; echo "== $1 $2 $(date -u +%H:%M:%S)"; nice -n 10 python3 out/job_ST111/k111chk.py $1 $2 2>&1 | cut -c1-500; done
echo CHKDONE $(date -u +%H:%M:%S)
