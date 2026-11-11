#!/bin/zsh
# ST-129: build the 6 R-queue modules deferred to the end (synth_active drops), after the main R workers finish. Reorder only: nothing skipped.
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
while pgrep -f "job_ST120R/queue_r2.sh|job_ST120R/worker3.sh" > /dev/null; do sleep 300; done
while read j m; do echo "build $m $(date -u +%H:%MZ)"; (cd $O/$j/lean && ./run.sh $m); done < $O/job_ST120R/deferred_st129.txt
echo TAILDONE
