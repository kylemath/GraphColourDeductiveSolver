#!/bin/zsh
# ST-119 Lean queue: after HDST111 ALLDONE, the 108 hD (HDST119) + 11 hC (HCST119) modules, largest ring first, NPAR (default 3), then the All modules
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q ALLDONE $O/job_HDST111/lean/status.txt 2>/dev/null; do sleep 120; done
echo "start $(date -u +%H:%MZ)"; (cd $O/job_HDST119/lean && ./run.sh HDST119)
cat $O/job_ST119/queue_order.txt | xargs -P ${NPAR:-3} -L 1 sh -c 'cd '$O'/$0/lean && ./run.sh $1'
(cd $O/job_HDST119/lean && ./run.sh HDST119All; echo ALLDONE >> status.txt)
(cd $O/job_HCST119/lean && ./run.sh ST119VAll; echo ALLDONE >> status.txt)
echo "QDONE $(date -u +%H:%MZ)"
