#!/bin/zsh
# ST-120 R queue: a third worker (coordinator 21:08Z: 4 Lean slots, extra slot to R). Same lock dir; stops new modules if free memory < 25 GB.
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
L=$O/job_ST120R/locks
while read j m r; do
  while [ "$(vm_stat | awk '/free|inactive|speculative/{s+=$NF} END{print int(s*16384/1e9)}')" -lt 25 ]; do sleep 120; done
  mkdir $L/$m 2>/dev/null || continue; (cd $O/$j/lean && ./run.sh $m)
done < $O/job_ST120R/queue_order.txt
echo W3DONE
