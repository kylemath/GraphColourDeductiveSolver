#!/bin/bash
# coordinator 10:34Z: switch MS6 to family l at the first iteration boundary after HCK5P05, HCK5P07, HDK5P08 are GLUEDONE (LP_ON_CHECK=1). Run detached.
W=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis
R=$HOME/maclane/maclane-k86; N=$R/fs/home/claude/GraphColourDeductiveSolver/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/loop/opus/P_own_lp/s86_f2b7
for j in HCK5P05 HCK5P07 HDK5P08; do until grep -q GLUEDONE $W/out/job_$j/lean/status.txt 2>/dev/null; do sleep 120; done; done
echo "all GLUEDONE $(date -u +%H:%M)"
K=$N/runK_k86MS6/K.log; n0=$(grep -c '^iter ' $K)
until [ "$(grep -c '^iter ' $K)" -gt "$n0" ]; do sleep 20; done
grep '^iter ' $K | tail -1 | cut -c1-110; echo "boundary $(date -u +%H:%M)"
cd $R; LP_ON_CHECK=1 bash launch_upper_fam.sh l
echo "launch exit $? $(date -u +%H:%M)"; echo SWITCHDONE
