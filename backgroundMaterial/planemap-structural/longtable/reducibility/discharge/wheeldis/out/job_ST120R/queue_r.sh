#!/bin/zsh
# ST-120 R queue (2 Lean slots): after HCK5P22 ALLDONE and the own-engine re-check, build HDRS403 / HCRS403, compile the
# base modules, then all V modules largest ring first at NPAR (default 2), then the All modules.
O=/Users/kylemathewson/GraphColourDeductiveSolver/.claude/worktrees/inspiring-lamport-831744/backgroundMaterial/planemap-structural/longtable/reducibility/discharge/wheeldis/out
until grep -q ALLDONE $O/job_HCK5P22/lean/status.txt 2>/dev/null && grep -q RSCHKDONE $O/job_ST120R/chk.log 2>/dev/null; do sleep 120; done
cd $O/..; python3 out/job_ST120R/build_r.py || { echo BUILDFAIL; exit 1; }
echo "start $(date -u +%H:%MZ)"; (cd $O/job_HDRS403/lean && ./run.sh HDRS403); (cd $O/job_HCRS403/lean && ./run.sh CKRS403)
tail -1 $O/job_HCRS403/lean/status.txt | grep -q "exit=0" || { echo "CKRS403 FAILED"; exit 1; }
cat $O/job_ST120R/queue_order.txt | xargs -P ${NPAR:-2} -L 1 sh -c 'cd '$O'/$0/lean && ./run.sh $1'
(cd $O/job_HDRS403/lean && ./run.sh HDRS403All; echo ALLDONE >> status.txt)
(cd $O/job_HCRS403/lean && ./run.sh RS403VAll; echo ALLDONE >> status.txt)
echo "QDONE $(date -u +%H:%MZ)"
