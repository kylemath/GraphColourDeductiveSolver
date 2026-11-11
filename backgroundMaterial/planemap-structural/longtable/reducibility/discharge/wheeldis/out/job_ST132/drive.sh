#!/bin/zsh
# ST-132: Lean for the 14 new W6b rotsub kills (13 hD + 1 hC), at the head of the queue: 2 workers, lock dir, 25 GB free floor.
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
(cd $O/job_HDST132/lean && ./run.sh HDST132) & (cd $O/job_HCST132/lean && ./run.sh CKST132) & wait
tail -1 $O/job_HCST132/lean/status.txt | grep -q "^CKST132 exit=0" || echo "CKST132 FAILED"
L=$O/job_ST132/locks; mkdir -p $L
worker(){ while read j m r; do
  while [ "$(vm_stat | awk '/free|inactive|speculative/{s+=$NF} END{print int(s*16384/1e9)}')" -lt 25 ]; do sleep 120; done
  mkdir $L/$m 2>/dev/null || continue; echo "build $m $(date -u +%H:%MZ)"; (cd $O/$j/lean && ./run.sh $m); done < $O/job_ST132/queue_order.txt; }
worker & sleep 5; worker & wait
(cd $O/job_HDST132/lean && ./run.sh HDST132All; echo ALLDONE >> status.txt)
(cd $O/job_HCST132/lean && ./run.sh ST132VAll; echo ALLDONE >> status.txt)
echo "QDONE $(date -u +%H:%MZ)"
