#!/bin/bash
# ST-110: start the bindt107 screen (4 procs) when ST-103 ends (ALLDONE in its run.log). Studio decision 12:00Z: load ~37/16 cores, so no early start.
J=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q ALLDONE $J/job_ST103/run.log 2>/dev/null; do sleep 120; done
cat $J/job_ST103/killed_rows.txt >> $J/job_ST110/killed_rows.txt; sort -u -o $J/job_ST110/killed_rows.txt $J/job_ST110/killed_rows.txt
echo "ST-103 ALLDONE seen $(date -u +%H:%MZ); starting ST-110 with $(cat $J/job_ST110/np.txt) procs"; bash $J/job_ST110/ctl.sh $(cat $J/job_ST110/np.txt); echo CHAINED
